import os
import pwd
import json
from yin_yang.plugins.plugin import Plugin, inplace_change

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/"+user+"/.config"


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
                        write_new_settings(settings, editor)
                    try:
                        old_theme = settings["workbench.colorTheme"]
                    except KeyError:
                        # happens when the default theme in vscode is used
                        write_new_settings(settings, editor)
                inplace_change(editor,
                               old_theme, theme)
