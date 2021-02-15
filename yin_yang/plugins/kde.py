import os
import pwd
import subprocess
from typing import Dict

from yin_yang.plugins.plugin import Plugin


translations = {}


class Kde(Plugin):
    name = 'KDE'
    # noinspection SpellCheckingInspection
    theme_bright = 'org.kde.breeze.desktop'
    # noinspection SpellCheckingInspection
    theme_dark = 'org.kde.breezedark.desktop'

    def get_themes_available(self) -> Dict[str, str]:
        return get_kde_theme_names()

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
        # noinspection SpellCheckingInspection
        subprocess.run(["lookandfeeltool", "-a", theme])


def get_short_name(file) -> str:
    """Searches for the long_name in the file and maps it to the found short name"""

    for line in file:
        if 'Name=' in line:
            name: str = ''
            write: bool = False
            for letter in line:
                if letter == '\n':
                    write = False
                if write:
                    name += letter
                if letter == '=':
                    write = True
            return name


def get_kde_theme_names():
    """
    Returns a name_map with translations for kde theme names.
    """

    global translations

    if translations != {}:
        return translations

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

    # asks the system what themes are available
    # noinspection SpellCheckingInspection
    long_names = subprocess.check_output(["lookandfeeltool", "-l"], universal_newlines=True)
    long_names = long_names.splitlines()

    # get the actual name
    for long_name in long_names:
        # trying to get the Desktop file
        try:
            # load the name from the metadata.desktop file
            with open('/usr/share/plasma/look-and-feel/{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                translations[long_name] = get_short_name(file)
        except OSError:
            # check the next path if the themes exist there
            try:
                # load the name from the metadata.desktop file
                with open('{path}{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                    # search for the name
                    translations[long_name] = get_short_name(file)
            except OSError:
                # if no file exist lets just use the long name
                translations[long_name] = long_name

    return translations
