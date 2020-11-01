import json
import os
import pathlib
import re
from enum import Enum
from typing import Optional

from main import assembly_version
from suntime import Sun, SunTimeException

# aliases for path to use later on
home = os.getenv("HOME")
path = home + "/.config"

# plugin categories are used in the gui
plugins = ["kde", "gnome", "gtk", "kvantum", "wallpaper",
           "firefox", "code", "atom"]


class Modes(Enum):
    manual = "manual"
    scheduled = "manual time"
    followSun = "sunset and sunrise"


def get_default():
    # if there is no config generate a generic one
    conf_default = {
        "version": assembly_version,
        "running": False,
        "theme": "",
        "soundEnabled": False,
        "desktop": get_desktop(),
        "mode": Modes.manual.value,
        "latitude": "",
        "longitude": "",
        "switchToDark": "20:00",
        "switchToLight": "07:00"
    }

    # plugin settings
    for plugin in plugins:
        conf_default[plugin] = {
            "enabled": False,
            "lightTheme": "",
            "darkTheme": ""
        }

    # default themes
    conf_default["code"]["LightTheme"] = "Default Light+"
    conf_default["code"]["DarkTheme"] = "Default Dark+"

    conf_default["kde"]["LightTheme"] = "org.kde.breeze.desktop"
    conf_default["kde"]["DarkTheme"] = "org.kde.breezedark.desktop"

    conf_default["firefox"]["DarkTheme"] = "firefox-compact-dark@mozilla.org"
    conf_default["firefox"]["LightTheme"] = "firefox-compact-light@mozilla.org"

    return conf_default


class ConfigParser:
    config: dict

    def __init__(self):
        # load config from file
        self.config = self.load()

        # use default values if something went wrong
        if self.config is None or self.config == {}:
            print("Using default values.")
            self.config = get_default()

        # check if config needs an update
        if self.config["version"] < assembly_version:
            self.update_config()

    def update_config(self):
        """Update old config files"""

        # replace current config with defaults
        config_old = self.config.copy()
        self.config = get_default()

        # replace default values with old ones
        if config_old["version"] <= 2.1:
            # determine mode
            if config_old["schedule"]:
                mode = Modes.scheduled.value
            elif config_old["followSun"]:
                mode = Modes.followSun.value
            else:
                mode = Modes.manual.value

            self.config["mode"] = mode

            # put settings for plugins into sections
            for plugin in plugins:
                for key in get_default()[plugin].keys():
                    self.config[plugin][key] = config_old[plugin + key.title()]

        # after all checks, update the version
        self.update("version", assembly_version)

        return config_old

    def load(self):
        """Load config from file or generate new one"""
        # generate path for yin-yang if there is none this will be skipped
        pathlib.Path(path + "/yin_yang").mkdir(parents=True, exist_ok=True)

        conf = {}

        # check if conf exists
        if os.path.isfile(path + "/yin_yang/yin_yang.json"):
            # load conf
            with open(path + "/yin_yang/yin_yang.json", "r") as conf:
                conf = json.load(conf)

        return conf

    def write(self):
        """Write configuration"""
        with open(path + "/yin_yang/yin_yang.json", 'w') as conf_file:
            json.dump(self.config, conf_file, indent=4)

    def get(self, key, plugin: Optional[str] = None):
        """Return the given key from the config"""
        if plugin is None:
            return self.config[key]
        else:
            return self.config[plugin][key]

    def update(self, key, value, plugin: Optional[str] = None):
        """Update the value of a key in configuration"""
        if plugin is None:
            self.config[key] = value
        else:
            self.config[plugin][key] = value
        self.write()

    def get_config(self):
        """returns the config"""
        return self.config


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


def set_sun_time(config: ConfigParser):
    latitude: float = float(config.get("latitude"))
    longitude: float = float(config.get("latitude"))
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        print('Today the sun raised at {} and get down at {}'.
              format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

        # Get today's sunrise and sunset in UTC
        config.update("switchToLight", today_sr.strftime('%H:%M'))
        config.update("switchToDark", today_ss.strftime('%H:%M'))

    except SunTimeException as e:
        print("Error: {0}.".format(e))
