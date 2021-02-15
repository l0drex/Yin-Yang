import os
import subprocess
import sys

from yin_yang.plugins.plugin import Plugin


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Sound(Plugin):
    name = 'Sound'
    theme_bright = './resources/light.wav'
    theme_dark = './resources/dark.wav'

    def set_theme(self, theme: str):
        # noinspection SpellCheckingInspection
        subprocess.run(["paplay", resource_path(theme)])
