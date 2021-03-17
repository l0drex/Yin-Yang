from configparser import ConfigParser
from pathlib import Path

from yin_yang.plugins.plugin import Plugin, get_stuff_in_dir


def get_file() -> str:
    # noinspection SpellCheckingInspection
    path = str(Path.home()) + '/.local/share/konsole/'
    files = get_stuff_in_dir(path, type='dir')

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
