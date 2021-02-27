import os
import json
from pathlib import Path

from yin_yang.plugins.plugin import Plugin, inplace_change


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
