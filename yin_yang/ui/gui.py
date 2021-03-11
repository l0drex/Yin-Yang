from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox

from yin_yang.ui.mainwindow import Ui_main_window
from yin_yang.config import config, Modes, PLUGINS


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
        self.ui.status_bar.showMessage("yin-yang: v" + str(config.version))

        # set the correct mode
        mode = config.mode
        self.ui.btn_enable.setChecked(mode != Modes.manual)

        if mode == Modes.followSun:
            self.ui.time.setVisible(False)
            self.ui.btn_sun.setChecked(True)
        else:
            # fix for both settings for follow sun and scheduled showing up when changing enabling
            self.ui.btn_schedule.setChecked(True)
            self.ui.location.setVisible(False)

        self.ui.toggle_sound.setChecked(config.get(plugin='sound', key='enabled'))
        self.ui.toggle_notification.setChecked(config.get(plugin='notification', key='enabled'))

        # sets the correct time based on config
        self.get_time()
        self.get_location()
        self.get_plugins()

    def get_time(self):
        time_light, time_dark = config.times

        # giving the time widget the values of the config
        self.ui.inp_time_light.setTime(time_light)
        self.ui.inp_time_dark.setTime(time_dark)

    def get_time_sun(self, checked):
        if not checked:
            return

        self.set_location()
        self.get_time()

    def get_location(self):
        # set correct coordinates
        coordinates = config.location
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

            widget.setChecked(config.get(plugin.name, "Enabled"))

            if plugin.name == 'KDE' and config.desktop != "kde":
                # make the widget invisible
                widget.setChecked(False)
                widget.setVisible(False)
                config.update('kde', 'enabled', False)

            if plugin.name == 'Gnome' and config.desktop != "gnome":
                # make the widget invisible
                widget.setChecked(False)
                widget.setVisible(False)
                config.update('enabled', False, plugin='gnome')

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
                            config.get(plugin=plugin.name, key=f'{theme}_theme')
                        ]
                    )
                    child.setCurrentIndex(index)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(config.get(plugin=plugin.name, key="light_theme"))
                children[1].setText(config.get(plugin=plugin.name, key="dark_theme"))

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
        if not self.ui.btn_enable.isChecked():
            config.mode = Modes.manual
        elif self.ui.btn_schedule.isChecked():
            config.mode = Modes.scheduled
        elif self.ui.btn_sun.isChecked():
            config.mode = Modes.followSun

        config.update('sound', 'enabled', self.ui.toggle_sound.isChecked())
        config.update('notification', 'enabled', self.ui.toggle_notification.isChecked())

        # set values of application config
        self.set_time()
        self.set_location()
        self.set_plugins()

    def set_time(self):
        """Sets the time set in the ui to the config"""

        # update config if time has changed
        time_light = self.ui.inp_time_light.time()
        time_dark = self.ui.inp_time_dark.time()
        config.times = time_light, time_dark

    def set_location(self):
        coordinates = [
            self.ui.inp_latitude.value(),
            self.ui.inp_longitude.value()
        ]
        config.location = coordinates

    def set_current_location(self):
        """Sets the current location to config and updates input field values"""

        config.set_auto_location(True)
        self.get_location()

    def set_plugins(self):
        for plugin in PLUGINS:
            # filter out all plugins for application
            if plugin.name.casefold() in ['notification', 'sound']:
                continue

            widget = self.ui.plugins_scroll_content.findChild(QtWidgets.QGroupBox, f'group{plugin.name}')

            config.update(plugin.name, 'enabled', widget.isChecked())
            if plugin.get_themes_available():
                # extra behaviour for combobox
                children = widget.findChildren(QtWidgets.QComboBox)
                for child in children:
                    theme = 'light' if children.index(child) == 0 else 'dark'
                    theme_name: str = list(plugin.get_themes_available().keys())[child.currentIndex()]
                    config.update(plugin.name, f'{theme}_theme', theme_name)
            else:
                children = widget.findChildren(QtWidgets.QLineEdit)
                config.update(plugin.name, "light_theme", children[0].text())
                config.update(plugin.name, "dark_theme", children[1].text())

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
