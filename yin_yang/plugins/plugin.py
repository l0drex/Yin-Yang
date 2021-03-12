import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLineEdit, QComboBox

logger = logging.getLogger(__name__)


class Plugin(ABC):
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

    def get_themes_available(self) -> Dict[str, str]:
        """Return a list of available themes
        :return: Dict[intern_name, readable_name]
        """
        return {}

    def set_mode(self, dark: bool):
        """Set the theme"""

        theme = self.theme_dark if dark else self.theme_bright
        logger.info(f'Switching theme to {theme} in {self.name}')
        self.set_theme(theme)

    @abstractmethod
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
        inputs = []

        if self.get_themes_available():
            # use a combobox
            inputs = [QComboBox(widget), QComboBox(widget)]

            # add all theme names
            for inp in inputs:
                for theme in self.get_themes_available().values():
                    inp.addItem(theme)

            return inputs

        for theme in ['Light', 'Dark']:
            inp = QLineEdit(widget)
            inp.setObjectName(f'inp_{theme}')
            inp.setPlaceholderText(_translate('MainWindow', f'{theme} Theme'))
            inputs.append(inp)

        return inputs


def inplace_change(filename, old_string, new_string):
    """@params: config - config to be written into file
                path - the path where the config is will be written into.
                    Defaults to the default path
    """
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        s = s.replace(old_string, new_string)
        f.write(s)
