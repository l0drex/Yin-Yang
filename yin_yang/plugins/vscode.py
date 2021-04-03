import os
import json
import logging
from pathlib import Path

from yin_yang.plugins.plugin import Plugin, get_stuff_in_dir


logger = logging.getLogger(__name__)


def write_new_settings(settings, path):
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
        paths = ['/usr/lib/code/extensions',
                 str(Path.home()) + '/.vscode-oss/extensions']
        themes_dict = {}

        for path in paths:
            extension_dirs = get_stuff_in_dir(path, type='dir')

            for extension_dir in extension_dirs:
                try:
                    with open(f'{path}/{extension_dir}/package.json', 'r') as file:
                        manifest = json.load(file)

                    try:
                        if 'Themes' not in manifest['categories']:
                            continue
                    except KeyError:
                        pass
                    try:
                        if 'themes' not in manifest['contributes']:
                            continue
                    except KeyError:
                        pass

                    try:
                        themes: list = manifest['contributes']['themes']

                        for theme in themes:
                            if 'id' in theme:
                                themes_dict[theme['id']] = theme['id']
                            else:
                                themes_dict[theme['label']] = theme['label']
                    except KeyError as e:
                        logger.error(str(e))
                        continue

                except FileNotFoundError as e:
                    logger.error(str(e))
                    if 'node_modules' in extension_dir:
                        logger.warning('Ignoring')
                        continue
                    themes_dict = {}
                    break

        assert themes_dict != {}, 'No themes found'
        return themes_dict
