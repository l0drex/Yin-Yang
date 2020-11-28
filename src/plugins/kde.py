import os
import pwd
import subprocess
from src.plugins.plugin import Plugin


class Kde(Plugin):
    name = 'KDE'
    theme_bright = 'org.kde.breeze.desktop'
    theme_dark = 'org.kde.breezedark.desktop'

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
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

    themes = {}

    # aliases for path to use later on
    user = pwd.getpwuid(os.getuid())[0]
    path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

    # asks the system what themes are available
    long_names = subprocess.check_output(["lookandfeeltool", "-l"], universal_newlines=True)
    long_names = long_names.splitlines()

    # get the actual name
    for long_name in long_names:
        # trying to get the Desktop file
        try:
            # load the name from the metadata.desktop file
            with open('/usr/share/plasma/look-and-feel/{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                themes[get_short_name(file)] = long_name
        except:
            # check the next path if the themes exist there
            try:
                # load the name from the metadata.desktop file
                with open('{path}{long_name}/metadata.desktop'.format(**locals()), 'r') as file:
                    # search for the name
                    themes[get_short_name(file)] = long_name
            except:
                # if no file exist lets just use the long_name name
                themes[long_name] = long_name

    return themes


def get_kde_theme_long(short: str):
    """
    Translates short names to long names.
    :param short: short name
    :return: long name
    """
    if short == '' or short is None:
        return
    themes = get_kde_theme_names()
    return themes[short]


def get_kde_theme_short(long: str):
    """
    Translates long names to short names.
    :param long: long name
    :return: short name
    """
    if long == '' or long is None:
        return
    themes = get_kde_theme_names()
    short_names = list(themes.keys())
    long_names = list(themes.values())
    return short_names[long_names.index(long)]
