import os
import subprocess
import sys

from src.plugins.plugin import Plugin


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Sound(Plugin):
    theme_bright = './assets/light.wav'
    theme_dark = './assets/dark.wav'

    def set_theme(self, theme: str):
        subprocess.run(["paplay", resource_path(theme)])
