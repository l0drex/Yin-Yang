import json
import logging
import os
import pathlib
import re
from datetime import time
from enum import Enum
from typing import Optional, Union, Tuple

import requests
from suntime import Sun, SunTimeException

from yin_yang.plugins.plugin import Plugin
from yin_yang.plugins import kde, gnome, gtk, kvantum, wallpaper, vscode, atom, sound, notify, konsole, firefox

logger = logging.getLogger(__name__)
ConfigValue = Union[str, float, bool, tuple]

# default objects
PLUGINS: [Plugin] = [kde.Kde(), gnome.Gnome(), gtk.Gtk(), kvantum.Kvantum(), wallpaper.Wallpaper(),
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


def get_default() -> dict:
    # if there is no config generate a generic one
    # NOTE: if you change or add new values here, make sure to update the version number and update_config() method
    conf_default = {
        "version": -1,
        "running": False,
        "dark_mode": False,
        "desktop": get_desktop(),
        "mode": Modes.manual.value,
        "listener": Listener.native.value,
        "coordinates": (0, 0),
        "switch_to_dark": "20:00",
        "switch_to_light": "07:00"
    }

    # plugin settings
    for plugin in PLUGINS:
        conf_default[plugin.name.casefold()] = {
            "enabled": False,
            "light_theme": plugin.theme_bright,
            "dark_theme": plugin.theme_dark
        }

    return conf_default


class ConfigParser:
    _config: dict = None
    _version: float
    debugging: bool = False
    changed: bool = False

    def __init__(self, version: float):
        self._version = version

        # load config from file
        self._config = self.load()

        if self._config is None:
            # use default values if something went wrong
            logger.warning('Using default configuration values.')
            self._config = get_default()
            self.update('version', self._version)

        # set plugin themes
        for plugin in PLUGINS:
            plugin.theme_bright = self.get('light_theme', plugin.name)
            plugin.theme_dark = self.get('dark_theme', plugin.name)

        # save the config
        self.write()

    def set_default(self):
        logger.info('Setting default values.')
        self._config = get_default()
        self.update("version", self._version)

    def update_config(self, config_old):
        """Update old config files
        Adds keys or restructures the config if an old config was loaded from the config file.
        Sets the new config directly to the dict in this class.

        :returns: the old config
        """

        logger.debug('Attempt to update the config file')

        # replace current config with defaults
        config_new = get_default()

        # replace default values with old ones
        if config_old["version"] < 0:
            return config_old
        if config_old["version"] <= 2.1:
            # determine mode
            if config_old["schedule"]:
                mode = Modes.scheduled.value
            elif config_old["followSun"]:
                mode = Modes.followSun.value
            else:
                mode = Modes.manual.value
            config_new["mode"] = mode

            # determine theme
            config_new["dark_mode"] = config_old["theme"] == "dark"

            # put settings for PLUGINS into sections
            for plugin in PLUGINS:
                for key in get_default()[plugin.name].keys():
                    key_old = key[0].upper() + key[1:]
                    config_new[plugin.name][key] = config_old[plugin.name.casefold() + key_old]
        self.changed = True
        return config_new

    def load(self) -> Optional[dict]:
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
            logger.warning('Could not load config file.')
            return None

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if 0 < config_loaded["version"] < self._version:
            return self.update_config(config_loaded)

        # no unsaved changes yet
        self.changed = False
        return config_loaded

    def write(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if not self.changed:
            logger.debug('No changes were made, skipping save')
            return False

        if self.debugging:
            logger.warning('Saving the config in debug mode is disabled!')
            return False

        logger.debug("Saving the config")
        try:
            with open(path + "/yin_yang/yin_yang.json", 'w') as conf_file:
                json.dump(self._config, conf_file, indent=4)

            # no unsaved changes anymore
            self.changed = False

            return True
        except IOError as e:
            logger.error(f"Error while writing the file: {e}")
            return False

    def get(self, key, plugin: Optional[str] = None) -> ConfigValue:
        """Return the given key from the config

        :param key: the key to change
        :param plugin: name of the plugin

        :returns: value
        """

        try:
            if plugin is None:
                return self._config[key.casefold()]
            else:
                return self._config[plugin.casefold()][key.casefold()]
        except KeyError as e:
            logger.warning(f"Unknown key {key}")
            if plugin is None:
                for p in PLUGINS:
                    if p.name.casefold() in key:
                        logger.warning("Key is deprecated. Use plugin option instead")
                        return self.get(key.replace(p.name, ''), plugin=p.name)
            else:
                raise e

    def update(self, key: str, value: ConfigValue, plugin: Optional[str] = None) -> ConfigValue:
        """Update the value of a key in configuration

        :param key: The setting to change
        :param value: The value to set the setting to
        :param plugin: Name of the plugin you may want to change

        :returns: new value
        """

        try:
            if plugin is None:
                self._config[key.casefold()] = value
            else:
                self._config[plugin.casefold()][key.casefold()] = value

            # new unsaved changes
            self.changed = True

            return self.get(key, plugin)
        except KeyError as e:
            logger.error(f'Error while updating {key}')
            raise e

    def get_config(self) -> dict:
        """returns the config"""

        return self._config


def get_desktop() -> str:
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


def get_current_location() -> Tuple[float, float]:
    """
    Returns the current location as a tuple (latitude, longitude)
    """
    loc = requests.get('http://www.ipinfo.io/loc').text.split(',')
    return float(loc[0]), float(loc[1])


def get_sun_time() -> Tuple[time, time]:
    """Sets the sunrise and sunset to config based on location"""
    latitude, longitude = config.get('coordinates')
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        return today_sr.time(), today_ss.time()

    except SunTimeException as e:
        logger.error("Error: {0}.".format(e))


# create global object with current version
# NOTE change the version here if the structure of the config file has been modified
config = ConfigParser(2.2)
