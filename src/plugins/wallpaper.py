import subprocess
from src import config
from src.plugins.plugin import Plugin


class Wallpaper(Plugin):
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # theme is actually the wallpaper

        if theme == '':
            subprocess.run(["notify-send", "looks like no light wallpaper is set"])
        else:
            if config.get_desktop() == "kde":
                subprocess.run(
                    ["sh", "/opt/yin-yang/src/change_wallpaper.sh", theme])
            if config.get_desktop() == "gtk":
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                                "picture-uri", "file://" + theme])
