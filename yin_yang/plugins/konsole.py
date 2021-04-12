import logging
from configparser import ConfigParser
from os.path import isdir
from pathlib import Path

from yin_yang.plugins.plugin import Plugin, get_stuff_in_dir

logger = logging.getLogger(__name__)


class Konsole(Plugin):
    name = 'Konsole'
    theme_dark = 'Breeze'
    theme_bright = 'BlackOnWhite'
    global_path = '/usr/share/konsole'

    def set_theme(self, theme: str):
        config = ConfigParser()
        # leave casing as is
        config.optionxform = str
        user_path = str(Path.home()) + '/.local/share/konsole'
        files = get_stuff_in_dir(user_path, type='file')
        # only take profiles
        files = [user_path + '/' + f for f in files if f.endswith('.profile')]

        assert len(files) > 0, 'No profiles found!'

        for config_file in files:
            config.read(config_file)

            try:
                config['Appearance']['ColorScheme'] = theme
            except KeyError as e:
                logger.warning(
                    f"""
                    No key {str(e)} found. Trying to add one. 
                    If this doesnt work, try to change the theme manually once.
                    """)

                if str(e) == '\'Appearance\'':
                    config.add_section('Appearance')
                else:
                    raise e

                with open(config_file, 'w+') as file:
                    config.write(file)

                self.set_theme(theme)
                logger.info('Success!')
                return

            with open(config_file, 'w') as file:
                config.write(file)

    def get_themes_available(self) -> dict[str, str]:
        if not self.available:
            return {}

        themes_machine = get_stuff_in_dir(self.global_path, type='file')
        themes_machine = [theme.replace('.colorscheme', '') for theme in themes_machine if theme.endswith('.colorscheme')]
        themes_machine.sort()

        themes_dict = {}
        config_parser = ConfigParser()

        for theme in themes_machine:
            config_parser.read(f'{self.global_path}/{theme}.colorscheme')
            theme_name = config_parser['General']['Description']
            themes_dict[theme] = theme_name

        assert themes_dict != {}, 'No themes found!'
        return themes_dict

    @property
    def available(self) -> bool:
        return isdir(self.global_path)
