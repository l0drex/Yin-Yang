import json
import os
import pathlib
import re
from enum import Enum
from typing import Optional, Union
from suntime import Sun, SunTimeException
from src.plugins import kde, gnome, gtk, kvantum, wallpaper, vscode, atom

ConfigValue = Union[str, float, bool]

# default objects
PLUGINS = [kde.Kde(), gnome.Gnome(), gtk.Gtk(), kvantum.Kvantum(), wallpaper.Wallpaper(),
           vscode.Vscode(), atom.Atom()]


class Modes(Enum):
    manual = "manual"
    scheduled = "manual time"
    followSun = "sunset and sunrise"


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
        "sound_enabled": False,
        "desktop": get_desktop(),
        "mode": Modes.manual.value,
        "latitude": 0.0,
        "longitude": 0.0,
        "switch_to_dark": "20:00",
        "switch_to_light": "07:00"
    }

    # plugin settings
    for plugin in PLUGINS:
        conf_default[plugin.name] = {
            "enabled": False,
            "light_theme": plugin.theme_bright,
            "dark_theme": plugin.theme_dark
        }

    return conf_default


class ConfigParser:
    config: dict = None
    debugging = False

    def __init__(self, version: float):
        # load config from file
        self.config = self.load()

        # use default values if something went wrong
        if self.config is None or self.config == {}:
            print("Using default values.")
            self.config = get_default()
            self.update("version", version)

        # check if config needs an update
        # if the default values are set, the version number is below 0
        if 0 < self.config["version"] < version:
            print("Updating config file.")
            self.update_config()

        # update times for sunset and sunrise
        if self.get("mode") == Modes.followSun:
            self.set_sun_time()

    def update_config(self):
        """Update old config files
        Adds keys or restructures the config if an old config was loaded from the config file.
        Sets the new config directly to the dict in this class.

        :returns: the old config
        """

        # replace current config with defaults
        config_old = self.config.copy()
        self.config = get_default()

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
            self.config["mode"] = mode

            # determine theme
            self.config["dark_mode"] = config_old["theme"] == "dark"

            # put settings for PLUGINS into sections
            for plugin in PLUGINS:
                for key in get_default()[plugin.name.casefold()].keys():
                    key_old = key[0].upper() + key[1:]
                    self.config[plugin.name.casefold()][key] = config_old[plugin.name.casefold() + key_old]
        return config_old

    def load(self) -> dict:
        """Load config from file"""

        # generate path for yin-yang if there is none this will be skipped
        pathlib.Path(path + "/yin_yang").mkdir(parents=True, exist_ok=True)

        conf = {}

        # check if conf exists
        if os.path.isfile(path + "/yin_yang/yin_yang.json"):
            # load conf
            with open(path + "/yin_yang/yin_yang.json", "r") as conf:
                conf = json.load(conf)

        return conf

    def write(self) -> bool:
        """Write configuration

        :returns: whether save was successful
        """

        if self.debugging:
            print('Saving the config in debug mode is disabled!')
            return False

        print("Saving the config")
        try:
            with open(path + "/yin_yang/yin_yang.json", 'w') as conf_file:
                json.dump(self.config, conf_file, indent=4)
            return True
        except IOError as e:
            print(f"Error while writing the file: {e}")
            return False

    def get(self, key, plugin: Optional[str] = None) -> ConfigValue:
        """Return the given key from the config

        :param key: the key to change
        :param plugin: name of the plugin

        :returns: value
        """

        try:
            if plugin is None:
                return self.config[key.casefold()]
            else:
                return self.config[plugin][key.casefold()]
        except KeyError as e:
            print(f"Unknown key {key}")
            if plugin is None:
                for p in PLUGINS:
                    if p.name.casefold() in key:
                        print("Key is deprecated. Use plugin option instead")
                        return self.get(key.replace(p.name, ''), plugin=p.name)
            else:
                raise e

    def update(self, key: str, value: ConfigValue, plugin: Optional[str] = None) -> ConfigValue:
        """Update the value of a key in configuration

        :param key: The setting to change
        :param value: The value to set the setting to
        :param plugin: Name of the plugin you may want to change

        :returns: old value
        """

        try:
            old = self.get(key, plugin)
            if plugin is None:
                self.config[key.casefold()] = value
            else:
                self.config[plugin.casefold()][key.casefold()] = value
            return old
        except KeyError as e:
            print(f'Error while updating {key}')
            raise e

    def get_config(self) -> dict:
        """returns the config"""

        return self.config

    def set_sun_time(self):
        """Sets the sunrise and sunset to config based on location"""
        latitude: float = float(self.get("latitude"))
        longitude: float = float(self.get("latitude"))
        sun = Sun(latitude, longitude)

        try:
            today_sr = sun.get_local_sunrise_time()
            today_ss = sun.get_local_sunset_time()

            print('Today the sun raised at {} and get down at {}'.
                  format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

            # Get today's sunrise and sunset in UTC
            self.update("switchToLight", today_sr.strftime('%H:%M'))
            self.update("switchToDark", today_ss.strftime('%H:%M'))

        except SunTimeException as e:
            print("Error: {0}.".format(e))


def get_desktop():
    """Return the current desktops name or 'unknown' if can't determine it"""
    # just to get all possible implementations of desktop variables
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

    if(gnome_re.search(env) or
       gnome_re.search(second_env) or gnome_re.search(third_env)):
        return "gtk"
    if(budgie_re.search(env) or
       budgie_re.search(second_env) or budgie_re.search(third_env)):
        return "gtk"
    if(kde_re.search(env) or
       kde_re.search(second_env) or kde_re.search(third_env)):
        return "kde"
    if(plasma_re.search(env) or
       plasma_re.search(second_env) or plasma_re.search(third_env)):
        return "kde"
    if(plasma5_re.search(env) or
       plasma5_re.search(second_env) or plasma5_re.search(third_env)):
        return "kde"
    return "unknown"


# create global object with current version
config = ConfigParser(2.2)
