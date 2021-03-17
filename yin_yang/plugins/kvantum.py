import subprocess
from os import listdir
from os.path import join, isdir

from yin_yang.plugins.plugin import Plugin


def get_files_in_dir(path: str):
    # copied from https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    return [f for f in listdir(path) if isdir(join(path, f))]



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
        themes = get_files_in_dir('/usr/share/Kvantum')
        themes_dict: dict = {}
        assert len(themes) > 0, 'No themes were found'

        themes.sort()
        for theme in themes:
            themes_dict[theme] = theme

        return themes_dict
