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
    theme_bright = 'Breath2-light'
    config = ConfigParser()
    config_file: str

    def __init__(self):
        super().__init__()
        self.config.optionxform = str
        self.config_file = get_file()
        self.config.read(self.config_file)

    def set_theme(self, theme: str):
        self.config['Appearance']['ColorScheme'] = theme

        with open(self.config_file, 'w') as file:
            self.config.write(file)
