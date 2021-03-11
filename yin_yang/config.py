import json
import logging
import os
import pathlib
import re
from datetime import time
from enum import Enum
from typing import Union

import requests
from suntime import Sun, SunTimeException

from yin_yang.plugins.plugin import Plugin as PluginClass
from yin_yang.plugins import kde, gnome, gtk, kvantum, wallpaper, vscode, atom, sound, notify, konsole, firefox

logger = logging.getLogger(__name__)

# default objects
PLUGINS: [PluginClass] = [kde.Kde(), gnome.Gnome(), gtk.Gtk(), kvantum.Kvantum(), wallpaper.Wallpaper(),
                          vscode.Vscode(), atom.Atom(), konsole.Konsole(), firefox.Firefox(),
                          sound.Sound(), notify.Notification()]


class Modes(Enum):
    manual = "manual"
    scheduled = "manual time"
    followSun = "sunset to sunrise"


class Listener(Enum):
    native = 'native'
    clight = 'clight'


# aliases for path to use later on
home = os.getenv("HOME")
path = home + "/.config"


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
    if config_old["version"] <= 2.1:
        # determine mode
        if config_old.pop('schedule'):
            mode = Modes.scheduled.value
        elif config_old.pop('followSun'):
            mode = Modes.followSun.value
        else:
            mode = Modes.manual.value
        config_new["mode"] = mode

        config_new["dark_mode"] = config_old.pop('theme') == "dark"

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


class ConfigParser:
    _config_data: dict = None

    def __init__(self):
        self.changed = False
        self._config_data = self.defaults

    def set_default(self):
        logger.info('Setting default values.')
        self._config_data = self.defaults

    def load(self) -> None:
        """Load config from file"""

        logger.debug('Loading config file')

        # generate path for yin-yang if there is none this will be skipped
        pathlib.Path(path + "/yin_yang").mkdir(parents=True, exist_ok=True)

        config_loaded = {}

        # check if conf exists
        if os.path.isfile(path + "/yin_yang/yin_yang.json"):
            # load conf
            with open(path + "/yin_yang/yin_yang.json", "r") as config_file:
                config_loaded = json.load(config_file)

        if config_loaded is None or config_loaded == {}:
            # use default values if something went wrong
            logger.warning('Using default configuration values.')
            config_loaded = self.defaults

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if config_loaded["version"] < self.defaults['version']:
            self.changed = True
            config_loaded = update_config(config_loaded, self.defaults)
        else:
            # no unsaved changes yet
            self.changed = False

        self._config_data = config_loaded

    def write(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if not self.changed:
            logger.debug('No changes were made, skipping save')
            return False

        logger.debug("Saving the config")
        try:
            with open(path + "/yin_yang/yin_yang.json", 'w') as conf_file:
                json.dump(self._config_data, conf_file, indent=4)

            # no unsaved changes anymore
            self.changed = False

            return True
        except IOError as e:
            logger.error(f"Error while writing the file: {e}")
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
            # new unsaved changes
            self.changed = True
            return self.get(plugin, key)
        except KeyError as e:
            logger.error(f'Error while updating {plugin}.{key}')
            raise e

    @property
    def defaults(self) -> dict:
        # NOTE: if you change or add new values here, make sure to update the version number and update_config() method
        conf_default = {
            "version": 2.2,
            "running": False,
            "dark_mode": False,
            "mode": Modes.manual.value,
            "listener": Listener.native.value,
            "coordinates": (0, 0),
            "update_location": False,
            "times": ("07:00", "20:00"),
            "plugins": {}
        }

        # plugin settings
        for pl in PLUGINS:
            conf_default["plugins"][pl.name.casefold()] = {
                "enabled": False,
                "light_theme": pl.theme_bright,
                "dark_theme": pl.theme_dark
            }

        return conf_default

    @property
    def data(self) -> dict:
        return self._config_data

    @property
    def version(self) -> float:
        return self._config_data['version']

    @property
    def running(self) -> bool:
        return self._config_data['running']

    @running.setter
    def running(self, running: bool):
        self._config_data['running'] = running

    @property
    def dark_mode(self) -> bool:
        return self._config_data['dark_mode']

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self._config_data['dark_mode'] = dark_mode

    @property
    def mode(self) -> Modes:
        mode_string = self._config_data['mode']

        for mode in list(Modes):
            if mode_string == mode.value:
                return mode

        raise ValueError('Unsupported mode!')

    @mode.setter
    def mode(self, mode: Modes):
        self._config_data['mode'] = mode.value

    @property
    def listener(self) -> Listener:
        listener_string = self._config_data['listener']

        for listener in list(Listener):
            if listener_string == listener.value:
                return listener

        raise ValueError('Unsupported mode!')

    @listener.setter
    def listener(self, listener: Listener):
        self._config_data['listener'] = listener.value

    @property
    def location(self) -> tuple[float, float]:
        if self._config_data['update_location']:
            loc = requests.get('http://www.ipinfo.io/loc').text.split(',')
            return float(loc[0]), float(loc[1])

        return self._config_data['coordinates']

    @location.setter
    def location(self, coordinates: tuple[float, float]):
        if self._config_data['update_location']:
            raise ValueError('Location is updated automatically!')

        self._config_data['coordinates'] = coordinates

    @property
    def update_location(self) -> bool:
        return self._config_data['update_location']

    @update_location.setter
    def update_location(self, enabled: bool):
        self._config_data['update_location'] = enabled

    @property
    def times(self) -> tuple[time, time]:
        if self.mode == Modes.followSun:
            # use times for sunrise and sunset
            latitude, longitude = config.location
            sun = Sun(latitude, longitude)

            try:
                today_sr = sun.get_local_sunrise_time()
                today_ss = sun.get_local_sunset_time()

                return today_sr.time(), today_ss.time()

            except SunTimeException as e:
                logger.error("Error: {0}.".format(e))

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
        env = str(os.getenv("GDMSESSION")).lower()
        second_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()
        third_env = str(os.getenv("XDG_CURRENT_DESKTOP")).lower()

        # these are the envs I will look for
        # feel free to add your Desktop and see if it works
        gnome_re = re.compile(r'gnome')
        budgie_re = re.compile(r'budgie')
        kde_re = re.compile(r'kde')
        plasma_re = re.compile(r'plasma')
        plasma5_re = re.compile(r'plasma5')

        if (gnome_re.search(env) or
                gnome_re.search(second_env) or gnome_re.search(third_env)):
            return "gtk"
        if (budgie_re.search(env) or
                budgie_re.search(second_env) or budgie_re.search(third_env)):
            return "gtk"
        if (kde_re.search(env) or
                kde_re.search(second_env) or kde_re.search(third_env)):
            return "kde"
        if (plasma_re.search(env) or
                plasma_re.search(second_env) or plasma_re.search(third_env)):
            return "kde"
        if (plasma5_re.search(env) or
                plasma5_re.search(second_env) or plasma5_re.search(third_env)):
            return "kde"
        return "unknown"


# create global object with current version
# NOTE change the version here if the structure of the config file has been modified
config = ConfigParser()
# load config from file
config.load()

# set plugin themes
for plugin in PLUGINS:
    plugin.theme_bright = config.get(plugin.name, 'light_theme')
    plugin.theme_dark = config.get(plugin.name, 'dark_theme')
