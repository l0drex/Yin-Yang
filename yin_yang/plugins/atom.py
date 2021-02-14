import os
import pwd
import re
from yin_yang.plugins.plugin import Plugin

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.atom/config.cson"


def inplace_change(filename, old_string, new_string):
    """@params: config - config to be written into file
                path - the path where the config is will be written into.
                    Defaults to the default path
    """
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print(
            'Changing "{old_string}" to "{new_string}" in {filename}'
            .format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)


def get_old_theme(settings):
    """returns the theme which is currently used
       uses regex to find the currently used theme
       i excpect that themes follow this pattern
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
