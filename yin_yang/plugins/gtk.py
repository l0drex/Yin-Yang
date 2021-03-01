import subprocess
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from yin_yang.plugins.plugin import Plugin


class Gtk(Plugin):
    name = 'GTK'
    theme_dark = ''
    theme_bright = ''

    def __init__(self, theme_dark: Optional[str] = None, theme_bright: Optional[str] = None):
        super().__init__(theme_dark, theme_bright)

        self._strategy = Gnome()

        # FIXME themes are not set correctly
        self.theme_bright = self._strategy.theme_bright
        self.theme_dark = self._strategy.theme_dark

    def use_kde(self):
        self._strategy = Kde()

    def set_theme(self, theme: str):
        self._strategy.set_theme(theme)


class Gnome(Plugin):
    # TODO set default theme names
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(
            ["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme])  # Applications theme


class Kde(Plugin):
    # Breeze theme uses qt color scheme
    theme_bright = 'Breeze'
    theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        config = ConfigParser()
        config_file = str(Path.home()) + "/.config/gtk-3.0/settings.ini"
        config.read(config_file)

        config['Settings']['gtk-theme-name'] = theme

        with open(config_file, "r") as file:
            config.write(file)
