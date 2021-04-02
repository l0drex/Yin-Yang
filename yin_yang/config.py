import json
import logging
import os
import pathlib
import re
from psutil import process_iter, NoSuchProcess
from datetime import datetime, time
from enum import Enum
from typing import Union

import requests
from suntime import Sun, SunTimeException

from yin_yang.plugins.plugin import Plugin as PluginClass, PluginDesktopDependent
from yin_yang.plugins import system, gtk, kvantum, wallpaper, vscode, atom, sound, notify, konsole, firefox

logger = logging.getLogger(__name__)

# default objects
PLUGINS: [PluginClass] = [system.System(), gtk.Gtk(), wallpaper.Wallpaper(), kvantum.Kvantum(),
                          vscode.Vscode(), atom.Atom(), konsole.Konsole(), firefox.Firefox(),
                          sound.Sound(), notify.Notification()]


class Modes(Enum):
    """Different modes for determining the theme that should be used"""

    manual = 'manual'
    scheduled = 'manual time'
    followSun = 'sunset to sunrise'


# aliases for path to use later on
home = str(pathlib.Path.home())
path = home + '/.config'


def update_config(config_old: dict, defaults: dict):
    """Update old config files
    Adds keys or restructures the config if an old config was loaded from the config file.
    Sets the new config directly to the dict in this class.

    :returns: the old config
    """

    logger.debug('Attempt to update the config file')

    # replace current config with defaults
    config_new = defaults

    # replace default values with previous ones
    if config_old['version'] <= 2.1:
        # determine mode
        if config_old.pop('schedule'):
            mode = Modes.scheduled.value
        elif config_old.pop('followSun'):
            mode = Modes.followSun.value
        else:
            mode = Modes.manual.value
        config_new['mode'] = mode

        config_new['dark_mode'] = config_old.pop('theme') == 'dark'

        # put settings for PLUGINS into sections
        plugins: dict = defaults['plugins']
        for plugin_name, plugin_config in plugins.items():
            for key in plugin_config.keys():
                try:
                    key_old = str(key).replace('_', ' ').title().replace(' ', '')
                    # code was renamed to vs code
                    if plugin_name == 'vs code':
                        plugin_config[key] = config_old['code' + key_old]
                        continue
                    plugin_config[key] = config_old[plugin_name.casefold() + key_old]
                except KeyError:
                    if plugin_name == 'sound' and key in ['light_theme', 'dark_theme']:
                        # this is expected since there is no theme
                        continue
                    logger.warning(f'Error while updating old config file. No value found for {plugin_name}.{key}')
                    logger.info('This is most likely because the plugin was added in a later version')
    return config_new


class ConfigManager:
    """Manages the configuration using the singleton pattern"""

    _config_data: dict = None

    def __init__(self):
        self._config_data = self.defaults
        self._last_location_update = None

    def set_default(self):
        """Resets all values to the defaults specified in the defaults property."""

        logger.info('Setting default values.')
        self._config_data = self.defaults

    def load(self) -> None:
        """Load config from file"""

        logger.debug('Loading config file')

        # generate path for yin-yang if there is none this will be skipped
        pathlib.Path(path + '/yin_yang').mkdir(parents=True, exist_ok=True)

        config_loaded = {}

        # check if conf exists
        if os.path.isfile(path + '/yin_yang/yin_yang.json'):
            # load conf
            with open(path + '/yin_yang/yin_yang.json', 'r') as config_file:
                config_loaded = json.load(config_file)

        if config_loaded is None or config_loaded == {}:
            # use default values if something went wrong
            logger.warning('Using default configuration values.')
            config_loaded = self.defaults

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if config_loaded['version'] < self.defaults['version']:
            config_loaded = update_config(config_loaded, self.defaults)

        self._config_data = config_loaded

    def write(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if not self.changed:
            logger.debug('No changes were made, skipping save')
            return True

        logger.debug('Saving the config')
        try:
            with open(path + '/yin_yang/yin_yang.json', 'w') as conf_file:
                json.dump(self._config_data, conf_file, indent=4)

            return True
        except IOError as e:
            logger.error(f'Error while writing the file: {e}')
            return False

    def get(self, plugin: str, key: str) -> Union[bool, str]:
        """Return the given key from the config
        :param plugin: name of the plugin
        :param key: the key to change
        :returns: value
        """

        plugin = plugin.casefold()
        key = key.casefold()

        return self._config_data['plugins'][plugin][key]

    def update(self, plugin: str, key: str, value: Union[bool, str]) -> Union[bool, str]:
        """Update the value of a key in configuration

        :param key: The setting to change
        :param value: The value to set the setting to
        :param plugin: Name of the plugin you may want to change

        :returns: new value
        """

        plugin = plugin.casefold()
        key = key.casefold()

        try:
            self._config_data['plugins'][plugin][key] = value
            return self.get(plugin, key)
        except KeyError as e:
            logger.error(f'Error while updating {plugin}.{key}')
            raise e

    @property
    def defaults(self) -> dict:
        """All default values"""

        # NOTE: if you change or add new values here, make sure to update the version number and update_config() method
        conf_default = {
            'version': 2.2,
            'running': False,
            'dark_mode': False,
            'mode': Modes.manual.value,
            'coordinates': (0, 0),
            'update_location': False,
            'update_interval': 60,
            'times': ('07:00', '20:00'),
            'plugins': {}
        }

        # plugin settings
        for pl in PLUGINS:
            conf_default['plugins'][pl.name.casefold()] = {
                'enabled': False,
                'light_theme': pl.theme_bright,
                'dark_theme': pl.theme_dark
            }

        return conf_default

    @property
    def changed(self):
        # compare data in dict to data in file
        current_config = self._config_data.copy()
        self.load()
        changed: bool = current_config != self._config_data
        self._config_data = current_config

        return changed

    @property
    def data(self) -> dict:
        """All config values. Only use this for testing purposes!"""

        return self._config_data

    @property
    def version(self) -> float:
        return self._config_data['version']

    @property
    def running(self) -> bool:
        """True, if yin yang is currently running"""

        # check if a process called yin_yang is running
        for process in process_iter():
            try:
                if 'yin-yang' in process.name():
                    return True
            except NoSuchProcess:
                pass
        return False

    @property
    def dark_mode(self) -> bool:
        """Currently used theme. Might be wrong on initial start."""

        return self._config_data['dark_mode']

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self._config_data['dark_mode'] = dark_mode
        self.write()

    @property
    def mode(self) -> Modes:
        """Mode that should be used to check wether dark mode should be active or not"""

        mode_string = self._config_data['mode']
        for mode in list(Modes):
            if mode_string == mode.value:
                return mode

        raise ValueError('Unsupported mode!')

    @mode.setter
    def mode(self, mode: Modes):
        self._config_data['mode'] = mode.value

    @property
    def location(self) -> tuple[float, float]:
        if self._config_data['update_location']:
            # Only update the location if the last time we visited that page
            # was during the last check

            # standard value
            seconds_since_last_update = self.update_interval + 2
            # if it was already updated once, calculate the time
            if self._last_location_update is not None:
                seconds_since_last_update = (datetime.now() - self._last_location_update).seconds

            if seconds_since_last_update > (self.update_interval - 3):
                logger.debug('Updating location.')
                logger.debug(f'Last location update was {seconds_since_last_update} seconds ago.')

                try:
                    loc = requests.get('https://www.ipinfo.io/loc').text.split(',')
                    # convert the strings to floats
                    loc: tuple[float] = [float(coordinate) for coordinate in loc]
                    assert len(loc) == 2, 'The returned location should have exactly 2 values.'
                    self._config_data['coordinates'] = loc
                    self.write()
                    self._last_location_update = datetime.now()
                except requests.exceptions.ConnectionError as e:
                    logger.warning('Could not update location. Please check your internet connection.')
                    logger.error(str(e))

        return self._config_data['coordinates']

    @location.setter
    def location(self, coordinates: tuple[float, float]):
        if self._config_data['update_location']:
            raise ValueError('Location is updated automatically!')
        elif self.mode != Modes.followSun:
            raise ValueError('Updating location while not in mode follow sun is forbidden')

        self._config_data['coordinates'] = coordinates

    @property
    def update_location(self) -> bool:
        """Wether the location should be updated automatically"""

        return self._config_data['update_location']

    @update_location.setter
    def update_location(self, enabled: bool):
        self._config_data['update_location'] = enabled

    @property
    def times(self) -> tuple[time, time]:
        """Times during which dark mode should be inactive"""

        if self.mode == Modes.followSun:
            # use times for sunrise and sunset
            latitude, longitude = config.location
            if latitude == longitude:
                logger.warning(f'Latitude and longitude are both {latitude}')
            else:
                logger.debug(f'Calculating sunset and sunrise at location {latitude}, {longitude}.')

            sun = Sun(latitude, longitude)
            try:
                today_sr = sun.get_local_sunrise_time()
                today_ss = sun.get_local_sunset_time()

                return today_sr.time(), today_ss.time()

            except SunTimeException as e:
                logger.error(f'Error: {e}.')

        # return time in config data
        time_light, time_dark = self._config_data['times']

        time_light = time.fromisoformat(time_light)
        time_dark = time.fromisoformat(time_dark)

        return time_light, time_dark

    @times.setter
    def times(self, times: tuple[time, time]):
        if self.mode == Modes.scheduled:
            self._config_data['times'] = times[0].isoformat(), times[1].isoformat()
        else:
            raise ValueError('Changing times is only allowed in mode scheduled!')

    @property
    def desktop(self) -> str:
        """Return the current desktops name or 'unknown' if can't determine it"""

        # just to get all possible implementations of desktop variables
        # noinspection SpellCheckingInspection
        env = str(os.getenv('GDMSESSION')).lower()
        second_env = str(os.getenv('XDG_CURRENT_DESKTOP')).lower()
        third_env = str(os.getenv('XDG_CURRENT_DESKTOP')).lower()

        # these are the envs I will look for
        # feel free to add your Desktop and see if it works
        gnome_re = re.compile(r'gnome')
        budgie_re = re.compile(r'budgie')
        kde_re = re.compile(r'kde')
        plasma_re = re.compile(r'plasma')
        plasma5_re = re.compile(r'plasma5')

        if (gnome_re.search(env) or
                gnome_re.search(second_env) or gnome_re.search(third_env)):
            return 'gtk'
        if (budgie_re.search(env) or
                budgie_re.search(second_env) or budgie_re.search(third_env)):
            return 'gtk'
        if (kde_re.search(env) or
                kde_re.search(second_env) or kde_re.search(third_env)):
            return 'kde'
        if (plasma_re.search(env) or
                plasma_re.search(second_env) or plasma_re.search(third_env)):
            return 'kde'
        if (plasma5_re.search(env) or
                plasma5_re.search(second_env) or plasma5_re.search(third_env)):
            return 'kde'
        return 'unknown'

    @property
    def update_interval(self) -> int:
        """Seconds that should pass until next check"""

        return self._config_data['update_interval']


# create global object with current version
# NOTE change the version here if the structure of the config file has been modified
config = ConfigManager()
# load config from file
config.load()

logger.info('Detected desktop:', config.desktop)

# set plugin themes
for p in PLUGINS:
    if isinstance(p, PluginDesktopDependent):
        p.set_strategy(config.desktop)


for p in PLUGINS:
    p.theme_bright = config.get(p.name, 'light_theme')
    p.theme_dark = config.get(p.name, 'dark_theme')
