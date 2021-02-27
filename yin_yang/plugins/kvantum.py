import subprocess
from yin_yang.plugins.plugin import Plugin


class Kvantum(Plugin):
    name = 'Kvantum'
    # TODO set default themes
    theme_bright = ''
    theme_dark = ''

    def set_theme(self, theme: str):
        # uses a kvantum manager cli to switch to a light theme
        print("Kvantum Light theme:", theme)
        # noinspection SpellCheckingInspection
        subprocess.run(["kvantummanager", "--set", theme])
