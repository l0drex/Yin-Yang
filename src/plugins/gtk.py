import subprocess
from src.plugins.plugin import Plugin


class Gtk(Plugin):
    # TODO set default theme names
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # gtk_theme = "Default"
        # uses a kde api to switch to a light theme
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme]) # Applications theme
        #subprocess.run(["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", '"{}"'.format(gtk_theme)]) # Shell theme
