from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox

from src.ui.mainwindow import Ui_MainWindow
from src.config import config, Modes, get_current_location, PLUGINS
from src.plugins import kde


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yin & Yang")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set the config values to the elements
        self.get_config()

        # connects all buttons to the correct routes
        self.register_handlers()

        # center the window
        self.center()

    def center(self):
        """Centers the window"""
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def close_event(self, event):
        """Overwrite the function that gets called when window is closed"""

        if self.should_close():
            event.accept()
        else:
            event.ignore()

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

    def register_handlers(self):
        # set sunrise and sunset times if mode is set to followSun or coordinates changed
        self.ui.buttonSun.toggled.connect(self.get_time_sun)
        self.ui.inLatitude.valueChanged.connect(self.get_time_sun)
        self.ui.inLongitude.valueChanged.connect(self.get_time_sun)

        # button to get the current position
        self.ui.buttonLocation.pressed.connect(self.set_current_location)

        # connect dialog buttons
        self.ui.buttonBox.clicked.connect(self.save_config)

        # TODO
        if False:
            self.ui.wallpaper_light_open.clicked.connect(self.set_wallpaper_light)
            self.ui.wallpaper_dark_open.clicked.connect(self.set_wallpaper_dark)

    def get_config(self):
        """Sets the values from the config to the elements"""

        # set current version in statusbar
        self.ui.statusBar.showMessage("yin-yang: v" + str(config.get("version")))

        # set the correct mode
        if config.get("mode") == Modes.scheduled.value:
            self.ui.buttonSchedule.setChecked(True)
        elif config.get("mode") == Modes.followSun.value:
            self.ui.buttonSun.setChecked(True)
        else:
            self.ui.buttonManual.setChecked(True)

        self.ui.enable_sound.setChecked(config.get('enabled', plugin='sound'))
        self.ui.enable_notification.setChecked(config.get('enabled', plugin='notification'))

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
        self.ui.inTimeDark.setTime(dark_time)
        self.ui.inTimeLight.setTime(light_time)

    def get_time_sun(self, checked):
        if not checked:
            return

        self.set_location()
        config.set_sun_time()
        self.get_time()

    def get_location(self):
        # set correct coordinates
        coordinates = config.get('coordinates')
        self.ui.inLatitude.setValue(coordinates[0])
        self.ui.inLongitude.setValue(coordinates[1])

    def get_plugins(self):
        widget: QtWidgets.QWidget
        for plugin in PLUGINS:
            widget = plugin.get_widget(self.ui.scrollAreaWidgetContents)
            self.ui.verticalLayout.addWidget(widget)

            assert widget is not None, f'No widget for plugin {plugin.name} found'

            widget.setChecked(config.get("Enabled", plugin=plugin.name))

            if plugin.name == 'KDE':
                if config.get("desktop") == "kde":
                    # use combobox instead of line edit
                    children = widget.findChildren(QtWidgets.QComboBox)
                    # append the names to the combobox
                    if config.get("desktop") == "kde":
                        if children[0].count() == 0 and children[1].count() == 0:
                            kde_themes = kde.get_kde_theme_names()

                            for name, theme in kde_themes.items():
                                for child in children:
                                    child.addItem(name)
                    else:
                        widget.setChecked(False)
                        config.update("kdeEnabled", False)

                    # set the index
                    index_dark = children[0].findText(
                        kde.get_kde_theme_short(config.get("Dark_Theme", plugin='kde')))
                    children[0].setCurrentIndex(index_dark)

                    index_light = children[1].findText(
                        kde.get_kde_theme_short(config.get("Light_Theme", plugin='kde')))
                    children[1].setCurrentIndex(index_light)
                else:
                    # make the widget invisible
                    widget.setChecked(False)
                    widget.setVisible(False)
                    config.update("Enabled", False, plugin='kde')
            else:
                if plugin.name == 'Gnome' and config.get("desktop") != "gnome":
                    # make the widget invisible
                    widget.setChecked(False)
                    widget.setVisible(False)
                    config.update("Enabled", False, plugin='gnome')

                children = widget.findChildren(QtWidgets.QLineEdit)
                children[0].setText(config.get("dark_theme", plugin=plugin.name))
                children[1].setText(config.get("light_theme", plugin=plugin.name))

    def set_config(self):
        """Sets the values to the config object, but does not save them"""

        # determine the mode to use
        if self.ui.buttonSchedule.isChecked():
            config.update('mode', Modes.scheduled.value)
        elif self.ui.buttonSun.isChecked():
            config.update('mode', Modes.followSun.value)
        else:
            config.update('mode', Modes.manual.value)

        config.update('enabled', self.ui.enable_sound.isChecked(), plugin='sound')
        config.update('enabled', self.ui.enable_notification.isChecked(), plugin='notification')

        # set values of application config
        self.set_time()
        self.set_location()
        self.set_plugins()

    def set_time(self):
        """Sets the time set in the ui to the config"""

        # update config if time has changed
        l_hour, l_minute = str(self.ui.inTimeLight.time().hour()), str(
            self.ui.inTimeLight.time().minute())
        d_hour, d_minute = str(self.ui.inTimeDark.time().hour()), str(
            self.ui.inTimeDark.time().minute())
        config.update("switch_To_Light", l_hour + ":" + l_minute)
        config.update("switch_To_Dark", d_hour + ":" + d_minute)

    def set_location(self):
        coordinates = [
            self.ui.inLatitude.value(),
            self.ui.inLongitude.value()
        ]
        config.update('coordinates', coordinates)

    def set_current_location(self):
        """Sets the current location to config and updates input field values"""

        config.update('coordinates', get_current_location())
        self.get_location()

    def set_plugins(self):
        # TODO this is kinda horrible

        # KDE
        config.update("enabled", self.ui.groupKde.isChecked(), plugin='kde')
        kde_light_short = self.ui.kde_light.currentText()
        config.update("light_theme", kde.get_kde_theme_long(kde_light_short), plugin='kde')
        kde_dark_short = self.ui.kde_dark.currentText()
        config.update("dark_theme", kde.get_kde_theme_long(kde_dark_short), plugin='kde')

        # Gnome
        config.update("enabled", self.ui.groupGnome.isChecked(), plugin='gnome')
        config.update("light_theme", self.ui.gnome_light.text(), plugin='gnome')
        config.update("dark_theme", self.ui.gnome_dark.text(), plugin='gnome')

        # gtk
        config.update("enabled", self.ui.groupGtk.isChecked(), plugin='gtk')
        config.update("light_theme", self.ui.gtk_light.text(), plugin='gtk')
        config.update("dark_theme", self.ui.gtk_dark.text(), plugin='gtk')

        # wallpaper
        config.update("enabled", self.ui.groupWallpaper.isChecked(), plugin='wallpaper')
        config.update('light_theme', self.ui.wallpaper_light.text(), plugin='wallpaper')
        config.update('dark_theme', self.ui.wallpaper_dark.text(), plugin='wallpaper')

        # vs code
        config.update("enabled", self.ui.groupVscode.isChecked(), plugin='vs code')
        config.update("light_theme", self.ui.code_light.text(), plugin='vs code')
        config.update("dark_theme", self.ui.code_dark.text(), plugin='vs code')

        # Kvantum
        config.update("enabled", self.ui.groupKvantum.isChecked(), plugin='Kvantum')
        config.update("light_theme", self.ui.kvantum_light.text(), plugin='Kvantum')
        config.update("dark_theme", self.ui.kvantum_dark.text(), plugin='Kvantum')

        # Atom
        config.update("enabled", self.ui.groupAtom.isChecked(), plugin='Atom')
        config.update("light_theme", self.ui.atom_light.text(), plugin='Atom')
        config.update("dark_theme", self.ui.atom_dark.text(), plugin='Atom')

    # TODO the following methods are very similar to each other, maybe there is a way to combine them
    def set_wallpaper_light(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Wallpaper Light", "")
        self.ui.wallpaper_light.setText(file_name)

    def set_wallpaper_dark(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Wallpaper Dark", "")
        self.ui.wallpaper_dark.setText(file_name)

    def save_config(self, button):
        """Saves the config to the file or restores values"""

        button = QDialogButtonBox.standardButton(self.ui.buttonBox, button)
        if button == QDialogButtonBox.Apply:
            self.set_config()
            return config.write()
        elif button == QDialogButtonBox.Reset:
            self.set_config()
            config.load()
            self.get_config()
        elif button == QDialogButtonBox.RestoreDefaults:
            config.set_default()
            self.get_config()
        else:
            raise ValueError(f'Unknown button {button}')
