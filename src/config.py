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


def exists():
    """returns True or False whether Config exists"""
    return os.path.isfile(path + "/yin_yang/yin_yang.json")


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


def set_sun_time():
    latitude: float = float(get("latitude"))
    longitude: float = float(get("latitude"))
    sun = Sun(latitude, longitude)

    try:
        today_sr = sun.get_local_sunrise_time()
        today_ss = sun.get_local_sunset_time()

        print('Today the sun raised at {} and get down at {}'.
              format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

        # Get today's sunrise and sunset in UTC
        update("switchToLight", today_sr.strftime('%H:%M'))
        update("switchToDark", today_ss.strftime('%H:%M'))

    except SunTimeException as e:
        print("Error: {0}.".format(e))


def get_default():
    # if there is no config generate a generic one
    config = {
        "version":          assembly_version,
        "running":          False,
        "theme":            "",
        "soundEnabled":     False,
        "desktop":          get_desktop(),
        "mode":             Modes.manual.value,
        "latitude":         "",
        "longitude":        "",
        "switchToDark":     "20:00",
        "switchToLight":    "07:00"
    }

    # plugin settings
    for plugin in plugins:
        config[plugin] = {
            "enabled": False,
            "lightTheme": "",
            "darkTheme": ""
        }

    # default themes
    config["code"]["LightTheme"] = "Default Light+"
    config["code"]["DarkTheme"] = "Default Dark+"

    config["kde"]["LightTheme"] = "org.kde.breeze.desktop"
    config["kde"]["DarkTheme"] = "org.kde.breezedark.desktop"

    config["firefox"]["DarkTheme"] = "firefox-compact-dark@mozilla.org"
    config["firefox"]["LightTheme"] = "firefox-compact-light@mozilla.org"

    return config


def update_config(old_config: dict):
    """Update old config files"""

    # replace current config with defaults
    config = get_default()

    # replace default values with old ones
    if old_config["version"] <= 2.1:
        # determine mode
        if old_config["schedule"]:
            mode = Modes.scheduled.value
        elif old_config["followSun"]:
            mode = Modes.followSun.value
        else:
            mode = Modes.manual.value

        config["mode"] = mode

        # put settings for plugins into sections
        for plugin in plugins:
            for key in get_default()[plugin].keys:
                config[plugin][key] = old_config[plugin+key.title()]

    # after all checks, update the version
    update("version", assembly_version)

    return config


def load_config():
    """Load config from file or generate new one"""
    # generate path for yin-yang if there is none this will be skipped
    pathlib.Path(path + "/yin_yang").mkdir(parents=True, exist_ok=True)

    # check if config exists
    if os.path.isfile(path + "/yin_yang/yin_yang.json"):
        # load config
        with open(path + "/yin_yang/yin_yang.json", "r") as conf:
            config = json.load(conf)

    if config["version"] < assembly_version:
        update_config()

    if config is None or config == {}:
        # use default values if something went wrong
        print("Using default values.")
        config = get_default()

    return config


# making config global
config = load_config()


def get(key, plugin: Optional[str]):
    """Return the given key from the config"""
    if plugin is None:
        return config[key]
    else:
        return config[plugin][key]


def get_config():
    """returns the config"""
    return config


def update(key, value, plugin: Optional[str]):
    """Update the value of a key in configuration"""
    if plugin is None:
        config[key] = value
    else:
        config[plugin][key] = value
    write_config()


def write_config(config=config):
    """Write configuration"""
    with open(path + "/yin_yang/yin_yang.json", 'w') as conf:
        json.dump(config, conf, indent=4)
