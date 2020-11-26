import subprocess
from src.plugins.plugin import Plugin


class Kvantum(Plugin):
    name = 'Kvantum'
    # TODO set default themes
    theme_bright = ''
    theme_dark = ''

    def set_theme(self, theme: str):
        # uses a kvantummanager cli to switch to a light theme
        print("Kvantum Light theme:", theme)
        subprocess.run(["kvantummanager", "--set", theme])
