import subprocess

from yin_yang.plugins.plugin import Plugin, get_stuff_in_dir


class Kvantum(Plugin):
    name = 'Kvantum'
    # TODO set default themes
    theme_bright = 'KvFlatLight'
    theme_dark = 'KvFlat'

    def set_theme(self, theme: str):
        # uses a kvantum manager cli to switch to a light theme
        print("Kvantum Light theme:", theme)
        # noinspection SpellCheckingInspection
        subprocess.run(["kvantummanager", "--set", theme])

    def get_themes_available(self) -> dict[str, str]:
        themes = get_stuff_in_dir('/usr/share/Kvantum', type='dir')
        themes_dict: dict = {}
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        for theme in themes:
            themes_dict[theme] = theme

        return themes_dict
