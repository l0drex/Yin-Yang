import subprocess
from src.plugins.plugin import Plugin

# WIP: Potential Check  for https://gist.github.com/atiensivu/fcc3183e9a6fd74ec1a283e3b9ad05f0 to reduce common issues, or write it in the FAQ


class Gnome(Plugin):
    name = 'Gnome'
    # TODO set the default theme for gnome
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # Shell theme
        subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name",
                        '"{}"'.format(theme)])
