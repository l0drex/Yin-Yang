import subprocess

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout

from yin_yang import config
from yin_yang.plugins.plugin import Plugin


class Wallpaper(Plugin):
    name = 'Wallpaper'
    theme_dark = ''
    theme_bright = ''

    def set_theme(self, theme: str):
        # theme is actually the wallpaper

        if config.get_desktop() == "kde":
            subprocess.run(["./scripts/change_wallpaper.sh", theme])
        if config.get_desktop() == "gtk":
            # noinspection SpellCheckingInspection
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                            "picture-uri", "file://" + theme])

    def get_input(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widgets = []

        for theme in ['light', 'dark']:
            grp = QtWidgets.QWidget(widget)
            horizontal_layout = QVBoxLayout(grp)

            inp = QtWidgets.QLineEdit(grp)
            inp.setPlaceholderText(_translate('MainWindow', f'{theme} theme'))
            horizontal_layout.addWidget(inp)

            btn = QtWidgets.QDialogButtonBox(grp)
            btn.setStandardButtons(QDialogButtonBox.Open)
            horizontal_layout.addWidget(btn)

            widgets.append(grp)

        return widgets
