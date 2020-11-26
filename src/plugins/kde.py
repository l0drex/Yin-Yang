import subprocess
from src.plugins.plugin import Plugin


class Kde(Plugin):
    theme_bright = 'org.kde.breeze.desktop'
    theme_dark = 'org.kde.breezedark.desktop'

    def set_theme(self, theme: str):
        # uses a kde api to switch to a light theme
        subprocess.run(["lookandfeeltool", "-a", theme])
