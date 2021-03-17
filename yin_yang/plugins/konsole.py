from configparser import ConfigParser
from os import listdir
from os.path import isfile, join
from pathlib import Path

from yin_yang.plugins.plugin import Plugin


def get_file() -> str:
    # noinspection SpellCheckingInspection
    path = str(Path.home()) + '/.local/share/konsole/'

    # copied from https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    files = [f for f in listdir(path) if isfile(join(path, f))]
    if len(files) == 1:
        return files[0]
    else:
        # TODO either return all profiles or return the standard profile
        return path + 'Fish.profile'


class Konsole(Plugin):
    name = 'Konsole'
    theme_dark = 'Breeze'
    theme_bright = 'BlackOnWhite'

    def set_theme(self, theme: str):
        config = ConfigParser()
        # leave casing as is
        config.optionxform = str
        config_file = get_file()
        config.read(config_file)

        config['Appearance']['ColorScheme'] = theme
        with open(config_file, 'w') as file:
            config.write(file)
