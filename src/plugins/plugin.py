from typing import Optional

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit


class Plugin:
    name = ''
    # default themes
    theme_dark = None
    theme_bright = None

    def __init__(self, theme_dark: Optional[str] = None, theme_bright: Optional[str] = None):
        # check default values
        if self.theme_dark is None or self.theme_bright is None:
            raise ValueError('Default value for theme is not set!')

        # set the themes
        if theme_dark is not None and theme_dark != self.theme_dark:
            self.theme_dark = theme_dark
        if theme_dark is not None and theme_bright != self.theme_bright:
            self.theme_bright = theme_bright

    def set_mode(self, dark: bool):
        """Set the theme"""
        if dark:
            print(f'Switching theme to {self.theme_dark} in {self.name}')
            self.set_theme(self.theme_dark)
        else:
            print(f'Switching theme to {self.theme_bright} in {self.name}')
            self.set_theme(self.theme_bright)

    def set_theme(self, theme: str):
        """Set a specific theme"""
        raise NotImplementedError('Function set_theme has not been implemented!')

    def get_widget(self, area) -> QGroupBox:
        """Returns a widget for the settings menu
        area: scrollAreaWidgetContents
        """

        widget = QGroupBox(area)
        widget.setCheckable(True)
        widget.setTitle(self.name)
        widget.setObjectName('group' + self.name)

        horizontal_layout = QHBoxLayout(widget)

        for inp in self.get_input(widget):
            horizontal_layout.addWidget(inp)

        return widget

    def get_input(self, widget):
        _translate = QtCore.QCoreApplication.translate

        widgets = []

        for theme in ['dark', 'light']:
            inp = QLineEdit(widget)
            inp.setObjectName(f'inp_{theme}')
            inp.setPlaceholderText(_translate('MainWindow', f'{theme} theme'))
            widgets.append(inp)

        return widgets
