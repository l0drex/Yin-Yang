from configparser import ConfigParser

from src.plugins.plugin import Plugin


class Konsole(Plugin):
    name = 'Konsole'
    theme_dark = 'Breeze'
    theme_bright = 'Breath2-light'
    config = ConfigParser()
    config_file = '/home/lorenzh/.local/share/konsole/Fish.profile'

    def __init__(self):
        super().__init__()
        self.config.optionxform = str
        self.config.read(self.config_file)

    def set_theme(self, theme: str):

        for section in self.config.sections():
            print(section)

        self.config['Appearance']['ColorScheme'] = theme

        with open(self.config_file, 'w') as file:
            self.config.write(file)
