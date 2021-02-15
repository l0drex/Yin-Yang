import os
import pwd
import re
import subprocess
from typing import Optional

from yin_yang.plugins.plugin import Plugin, inplace_change

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config/gtk-3.0"


class Gtk(Plugin):
    name = 'GTK'
    theme_dark = ''
    theme_bright = ''

    def __init__(self, theme_dark: Optional[str] = None, theme_bright: Optional[str] = None):
        super().__init__(theme_dark, theme_bright)

        self._strategy = Standard()

        # FIXME themes are not set correctly
        self.theme_bright = self._strategy.theme_bright
        self.theme_dark = self._strategy.theme_dark

    def use_kde(self):
        self._strategy = Kde()

    def set_theme(self, theme: str):
        self._strategy.set_theme(theme)


class Standard(Plugin):
    # TODO set default theme names
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(
            ["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme])  # Applications theme


class Kde(Plugin):
    theme_bright = 'Breeze'
    theme_dark = 'Breeze'

    def set_theme(self, theme: str):
        with open(path + "/settings.ini", "r") as file:
            # search for the theme section and change it
            current_theme = re.findall(
                'gtk-theme-name=[A-z -]*', str(file.readlines()))[0][:-2]
            inplace_change(path + "/settings.ini", current_theme, "gtk-theme-name=" + theme)
