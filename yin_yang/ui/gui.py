from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox

from yin_yang.ui.mainwindow import Ui_main_window
from yin_yang.config import config, Modes, get_current_location, PLUGINS


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # basic setup
        self.setWindowTitle("Yin & Yang")
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # center the window
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

        # set the config values to the elements
        self.get_config()

        # connects all buttons to the correct routes
        self.register_handlers()

    def get_config(self):
        """Sets the values from the config to the elements"""

        # set current version in statusbar
        self.ui.status_bar.showMessage("yin-yang: v" + str(config.get("version")))

        # set the correct mode
        if config.get("mode") == Modes.scheduled.value:
            self.ui.btn_schedule.setChecked(True)
        elif config.get("mode") == Modes.followSun.value:
            self.ui.btn_sun.setChecked(True)
        else:
            self.ui.btn_enable.setChecked(False)

        self.ui.toggle_sound.setChecked(config.get('enabled', plugin='sound'))
        self.ui.toggle_notification.setChecked(config.get('enabled', plugin='notification'))

        # sets the correct time based on config
        self.get_time()
        self.get_location()
        self.get_plugins()

    def get_time(self):
        d_hour = config.get("switch_To_Dark").split(":")[0]
        d_minute = config.get("switch_To_Dark").split(":")[1]
        l_hour = config.get("switch_To_Light").split(":")[0]
        l_minute = config.get("switch_To_Light").split(":")[1]

        # giving the time widget the values of the config
        dark_time = QTime(int(d_hour), int(d_minute))
        light_time = QTime(int(l_hour), int(l_minute))
        self.ui.inp_time_dark.setTime(dark_time)
        self.ui.inp_time_light.setTime(light_time)

    def get_time_sun(self, checked):
        if not checked:
            return

        self.set_location()
        self.get_time()

    def get_location(self):
        # set correct coordinates
        coordinates = config.get('coordinates')
        self.ui.inp_latitude.setValue(coordinates[0])
        self.ui.inp_longitude.setValue(coordinates[1])

    def get_plugins(self):
        widget: QtWidgets.QWidget
        for plugin in PLUGINS:
            # filter out plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'group'+plugin.name)
            if widget is None:
                widget = plugin.get_widget(self.ui.plugins_scroll_content)
                self.ui.plugins_scroll_content_layout.addWidget(widget)

            assert widget is not None, f'No widget for plugin {plugin.name} found'

            widget.setChecked(config.get("Enabled", plugin=plugin.name))

            if plugin.name == 'KDE' and config.get("desktop") != "kde":
                # make the widget invisible
                widget.setChecked(False)
                widget.setVisible(False)
                config.update("Enabled", False, plugin='kde')

            if plugin.name == 'Gnome' and config.get("desktop") != "gnome":
                # make the widget invisible
                widget.setChecked(False)
                widget.setVisible(False)
                config.update("Enabled", False, plugin='gnome')

            if plugin.name == 'Wallpaper':
                children = widget.findChildren(QtWidgets.QPushButton)
                children[0].clicked.connect(lambda: self.set_wallpaper(False))
                children[1].clicked.connect(lambda: self.set_wallpaper(True))

            if plugin.get_themes_available():
                # uses combobox instead of line edit
                # set the index
                for child in widget.findChildren(QtWidgets.QComboBox):
                    theme = 'light' if widget.findChildren(QtWidgets.QComboBox).index(child) == 0 else 'dark'
                    index = child.findText(
                        plugin.get_themes_available()[
                            config.get(f'{theme}_theme', plugin=plugin.name)
                        ]
                    )
                    child.setCurrentIndex(index)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(config.get("light_theme", plugin=plugin.name))
                children[1].setText(config.get("dark_theme", plugin=plugin.name))

    def register_handlers(self):
        # set sunrise and sunset times if mode is set to followSun or coordinates changed
        self.ui.btn_sun.toggled.connect(self.get_time_sun)
        self.ui.inp_latitude.valueChanged.connect(self.get_time_sun)
        self.ui.inp_longitude.valueChanged.connect(self.get_time_sun)

        # button to get the current position
        self.ui.btn_location.pressed.connect(self.set_current_location)

        # connect dialog buttons
        self.ui.btn_box.clicked.connect(self.save_config)

    def set_config(self):
        """Sets the values to the config object, but does not save them"""

        # determine the mode to use
        if self.ui.btn_schedule.isChecked():
            config.update('mode', Modes.scheduled.value)
        elif self.ui.btn_sun.isChecked():
            config.update('mode', Modes.followSun.value)
        else:
            config.update('mode', Modes.manual.value)

        config.update('enabled', self.ui.toggle_sound.isChecked(), plugin='sound')
        config.update('enabled', self.ui.toggle_notification.isChecked(), plugin='notification')

        # set values of application config
        self.set_time()
        self.set_location()
        self.set_plugins()

    def set_time(self):
        """Sets the time set in the ui to the config"""

        # update config if time has changed
        time_light = self.ui.inp_time_light.time()
        time_dark = self.ui.inp_time_dark.time()
        config.update("switch_To_Light", time_light.toString()[0:5])
        config.update("switch_To_Dark", time_dark.toString()[0:5])

    def set_location(self):
        coordinates = [
            self.ui.inp_latitude.value(),
            self.ui.inp_longitude.value()
        ]
        config.update('coordinates', coordinates)

    def set_current_location(self):
        """Sets the current location to config and updates input field values"""

        config.update('coordinates', get_current_location())
        self.get_location()

    def set_plugins(self):
        for plugin in PLUGINS:
            # filter out all plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, f'group{plugin.name}')

            config.update("enabled", widget.isChecked(), plugin=plugin.name)
            if plugin.get_themes_available():
                # extra behaviour for combobox
                children = widget.findChildren(QtWidgets.QComboBox)
                for child in children:
                    theme = 'light' if children.index(child) == 0 else 'dark'
                    theme_name: str = list(plugin.get_themes_available().keys())[child.currentIndex()]
                    config.update(f'{theme}_theme', theme_name, plugin=plugin.name)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                config.update("light_theme", children[0].text(), plugin=plugin.name)
                config.update("dark_theme", children[1].text(), plugin=plugin.name)

    def set_wallpaper(self, dark: bool):
        file_name, _ = QFileDialog.getOpenFileName(
            self, f"Open Wallpaper {'dark' if dark else 'light'}",
            str(Path.home()), "Images (*.png *.jpg *.jpeg *.JPG *.JPEG)")

        group_wallpaper = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, 'groupWallpaper')
        inputs_wallpaper = group_wallpaper.findChildren(QtWidgets.QLineEdit)
        i = 1 if dark else 0
        inputs_wallpaper[i].setText(file_name)

    def save_config(self, button):
        """Saves the config to the file or restores values"""

        button = QDialogButtonBox.standardButton(self.ui.btn_box, button)
        if button == QDialogButtonBox.Apply:
            self.set_config()
            return config.write()
        elif button == QDialogButtonBox.RestoreDefaults:
            config.set_default()
            self.get_config()
        elif button == QDialogButtonBox.Cancel:
            self.close()
        else:
            raise ValueError(f'Unknown button {button}')

    def should_close(self) -> bool:
        """Returns true if the user wants to close the application"""

        # ask the user if he wants to save changes
        if config.changed:
            ret = QMessageBox.warning(self, 'Unsaved changes',
                                      'The settings have been modified. Do you want to save them?',
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return config.write()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def close(self):
        """Overwrite the function that gets called when window is closed"""

        if self.should_close():
            super().close()
        else:
            pass
