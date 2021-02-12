import subprocess

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialogButtonBox

from src import config
from src.plugins.plugin import Plugin


class Wallpaper(Plugin):
    name = 'Wallpaper'
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
                # noinspection SpellCheckingInspection
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                                "picture-uri", "file://" + theme])

    def get_input(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widgets = []

        for theme in ['light', 'dark']:
            grp = QtWidgets.QWidget(widget)

            inp = QtWidgets.QLineEdit(grp)
            inp.setPlaceholderText(_translate('MainWindow', f'{theme} theme'))

            btn = QtWidgets.QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)

            widgets.append(grp)

        return widgets
