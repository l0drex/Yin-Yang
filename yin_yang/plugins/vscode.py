import os
import json
from pathlib import Path

from yin_yang.plugins.plugin import Plugin, get_stuff_in_dir


def write_new_settings(settings, path):
    print("SETTINGS ", len(settings))
    # simple adds a new field to the settings
    settings["workbench.colorTheme"] = "Default"
    with open(path, 'w') as conf:
        json.dump(settings, conf, indent=4)


class Vscode(Plugin):
    name = 'VS Code'
    theme_bright = 'Default Light+'
    theme_dark = 'Default Dark+'

    def set_theme(self, theme: str):
        path = str(Path.home()) + "/.config"

        possible_editors = [
            path + "/VSCodium/User/settings.json",
            path + "/Code - OSS/User/settings.json",
            path + "/Code/User/settings.json",
            path + "/Code - Insiders/User/settings.json",
        ]

        for editor in possible_editors:
            if os.path.isfile(editor):
                # getting the old theme to replace it
                with open(editor, "r") as sett:
                    try:
                        settings = json.load(sett)
                    except json.decoder.JSONDecodeError:
                        settings = {"workbench.colorTheme": ""}
                settings['workbench.colorTheme'] = theme
                with open(editor, 'w') as sett:
                    json.dump(settings, sett)

    def get_themes_available(self) -> dict[str, str]:
        try:
            path = '/usr/lib/code/extensions'
            theme_packages = get_stuff_in_dir(path, type='dir')
            theme_packages = [package_name.replace('theme-', '')
                              for package_name in theme_packages
                              if package_name.startswith('theme-')]
            assert len(theme_packages) > 0
            theme_packages.sort()

            themes_dict: dict = {}

            for package_name in theme_packages:
                with open(f'{path}/theme-{package_name}/package.json', 'r') as file:
                    package_metadata = json.load(file)
                try:
                    theme_ids = package_metadata['contributes']['themes']
                    # only take the ids
                    theme_ids = [theme_meta['id'] for theme_meta in theme_ids]

                    for theme_id in theme_ids:
                        themes_dict[theme_id] = theme_id
                except KeyError:
                    continue

            return themes_dict
        except FileNotFoundError:
            return {}
