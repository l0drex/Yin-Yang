import json
from pathlib import Path

from yin_yang.plugins.plugin import Plugin

# TODO more general please
path = str(Path.home()) + '/.mozilla/firefox/sooi88to.default-release/extensions.json'


class Firefox(Plugin):
    name = 'Firefox'
    theme_bright = 'firefox-compact-light@mozilla.org'
    theme_dark = 'firefox-compact-dark@mozilla.org'

    def set_theme(self, theme: str):
        pass

    def get_themes_available(self) -> dict[str, str]:
        themes: dict[str, str] = {}

        with open(path, 'r') as file:
            content = json.load(file)
            for addon in content['addons']:
                if addon['type'] == 'theme':
                    themes[addon['id']] = addon['defaultLocale']['name']

        return themes
