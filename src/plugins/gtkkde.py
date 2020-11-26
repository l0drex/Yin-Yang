import pwd
import os
import re
from src.plugins.plugin import Plugin

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config/gtk-3.0"


def inplace_change(filename, old_string, new_string):
    """@params: config - config to be written into file
               path - the path where the config is will be written into
                defaults to the default path

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


class GtkKde(Plugin):
    name = 'GTK'
    theme_bright = 'Breeze'
    theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        with open(path + "/settings.ini", "r") as file:
            # search for the theme section and change it
            current_theme = re.findall(
                'gtk-theme-name=[A-z -]*', str(file.readlines()))[0][:-2]
            inplace_change(path + "/settings.ini",
                           current_theme, "gtk-theme-name=" + theme)
