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
        return path + 'Bash.profile'


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

    def get_themes_available(self) -> dict[str, str]:
        try:
            path = '/usr/share/konsole'
            themes_machine = get_stuff_in_dir(path, type='file')
            themes_machine = [theme.replace('.colorscheme', '') for theme in themes_machine if theme.endswith('.colorscheme')]
            themes_machine.sort()

            themes_dict = {}
            config_parser = ConfigParser()

            for theme in themes_machine:
                config_parser.read(f'{path}/{theme}.colorscheme')
                theme_name = config_parser['General']['Description']
                themes_dict[theme] = theme_name

            return themes_dict
        except FileNotFoundError:
            return {}
