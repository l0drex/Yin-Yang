import os
import pwd
import re
from yin_yang.plugins.plugin import Plugin, inplace_change

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/" + user + "/.atom/config.cson"


def get_old_theme(settings):
    """returns the theme which is currently used
       uses regex to find the currently used theme
       i expect that themes follow this pattern
       XXXX-XXXX-ui     XXXX-XXXX-syntax
    """
    with open(settings, "r") as file:
        string = file.read()
        # themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
        themes = re.findall(r'themes: \[[\s]*"([A-Za-z0-9\-]*)"[\s]*"([A-Za-z0-9\-]*)"', string)
        if len(themes) >= 1:
            ui_theme, syntax_theme = themes[0]
            used_theme = re.findall("([A-z\-A-z]*)\-", ui_theme)[0]
            print(used_theme)
            return used_theme


class Atom(Plugin):
    name = 'Atom'
    # TODO set default themes
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # getting the old theme first
        current_theme = get_old_theme(path)

        # updating the old theme with theme specified in config
        inplace_change(path, current_theme, theme)
