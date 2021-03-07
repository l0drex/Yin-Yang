from yin_yang.plugins.plugin import Plugin


class Firefox(Plugin):
    name = 'Firefox'
    theme_bright = 'firefox-compact-light@mozilla.org'
    theme_dark = 'firefox-compact-dark@mozilla.org'

    def set_theme(self, theme: str):
        pass
