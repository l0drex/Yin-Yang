import subprocess
import pwd
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog
from src.ui.mainwindow import Ui_MainWindow
from src.ui.settings import Ui_PluginWindow as Ui_SettingsWindow
from src import yin_yang
from src import config

configParser = config.ConfigParser(-1)


class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plugins")
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        # center the settings window
        self.center()
        # syncing with config - fill out all fields based on Config
        self.sync_with_config()
        # register all the handler onClick functions ...
        self.register_handlers()

    def close_event(self, event):
        """Overwrite the function that gets called when window is closed"""
        self.save_and_exit()

    def save_and_exit(self):
        print("saving options")

        # system wide

        kde_light_short = self.ui.kde_combo_light.currentText()
        kde_dark_short = self.ui.kde_combo_dark.currentText()
        configParser.update("kdeLight_Theme",
                      self.get_kde_theme_long(kde_light_short))
        configParser.update("kdeDark_Theme", self.get_kde_theme_long(kde_dark_short))
        configParser.update("kdeEnabled", self.ui.groupKde.isChecked())

        configParser.update("gnomeEnabled", self.ui.groupGnome.isChecked())
        configParser.update("gnomeLight_Theme", self.ui.gnome_lineEdit_light.text())
        configParser.update("gnomeDark_Theme", self.ui.gnome_lineEdit_dark.text())

        configParser.update("gtkLight_Theme", self.ui.gtk_line_light.text())
        configParser.update("gtkDark_Theme", self.ui.gtk_line_dark.text())
        configParser.update("gtkEnabled", self.ui.groupGtk.isChecked())

        configParser.update("wallpaperEnabled", self.ui.groupWallpaper.isChecked())

        # single applications

        configParser.update("firefoxEnabled", self.ui.groupFirefox.isChecked())
        configParser.update("firefoxDark_Theme", self.ui.firefox_line_dark.text())
        configParser.update("firefoxLight_Theme", self.ui.firefox_line_light.text())

        configParser.update("codeLight_Theme", self.ui.code_line_light.text())
        configParser.update("codeDark_Theme", self.ui.code_line_dark.text())
        configParser.update("codeEnabled", self.ui.groupVscode.isChecked())

        configParser.update("kvantumLight_Theme", self.ui.kvantum_line_light.text())
        configParser.update("kvantumDark_Theme", self.ui.kvantum_line_dark.text())
        configParser.update("kvantumEnabled", self.ui.groupKvantum.isChecked())

        configParser.update("atomLight_Theme", self.ui.atom_line_light.text())
        configParser.update("atomDark_Theme", self.ui.atom_line_dark.text())
        configParser.update("atomEnabled", self.ui.groupAtom.isChecked())

        # showing the main window and hiding the current one
        self.hide()
        self.window = MainWindow()
        self.window.show()

    def register_handlers(self):
        self.ui.wallpaper_button_light.clicked.connect(
            self.open_wallpaper_light)
        self.ui.wallpaper_button_dark.clicked.connect(self.open_wallpaper_dark)
        self.ui.buttonBack.clicked.connect(self.save_and_exit)

    def sync_with_config(self):
        # sync config label with get the correct version
        self.ui.statusBar.showMessage("yin-yang: v" +
                                      str(configParser.get("version")))

        # syncing all fields and checkboxes with config

        # system wide
        # ---- KDE -----
        # reads out all kde themes and displays them inside a combobox
        if configParser.get("desktop") == "kde":
            self.ui.groupKde.setChecked(configParser.get("kdeEnabled"))
            # fixed bug where themes get appended multiple times
            self.get_kde_themes()
            index_light = self.ui.kde_combo_light.findText(
                self.get_kde_theme_short(configParser.get("kdeLight_Theme")))
            self.ui.kde_combo_light.setCurrentIndex(index_light)
            index_dark = self.ui.kde_combo_dark.findText(
                self.get_kde_theme_short(configParser.get("kdeDark_Theme")))
            self.ui.kde_combo_dark.setCurrentIndex(index_dark)
        else:
            self.ui.groupKde.setChecked(False)
            self.ui.groupKde.setEnabled(False)
            configParser.update("kdeEnabled", False)

        # Gnome
        if configParser.get("desktop") == "gnome":
            self.ui.gnome_lineEdit_dark.setText(configParser.get("gnomeDark_Theme"))
            self.ui.gnome_lineEdit_light.setText(configParser.get("gnomeLight_Theme"))
            self.ui.groupGnome.setChecked(configParser.get("gnomeEnabled"))
        else:
            self.ui.groupGnome.setChecked(False)
            self.ui.groupGnome.setEnabled(False)
            configParser.update("gnomeEnabled", False)
        # ---- GTK -----
        self.ui.gtk_line_light.setText(configParser.get("gtkLight_Theme"))
        self.ui.gtk_line_dark.setText(configParser.get("gtkDark_Theme"))
        self.ui.groupGtk.setChecked(configParser.get("gtkEnabled"))
        # Kvantum
        self.ui.kvantum_line_light.setText(configParser.get("kvantumLight_Theme"))
        self.ui.kvantum_line_dark.setText(configParser.get("kvantumDark_Theme"))
        self.ui.groupKvantum.setChecked(configParser.get("kvantumEnabled"))
        # ----- wallpaper --------
        self.ui.groupWallpaper.setChecked(configParser.get("wallpaperEnabled"))

        # applications

        # ---- VSCode ----
        self.ui.code_line_light.setText(configParser.get("codeLight_Theme"))
        self.ui.code_line_dark.setText(configParser.get("codeDark_Theme"))
        self.ui.groupVscode.setChecked(configParser.get("codeEnabled"))
        # ----- Atom --------
        self.ui.atom_line_light.setText(configParser.get("atomLight_Theme"))
        self.ui.atom_line_dark.setText(configParser.get("atomDark_Theme"))
        self.ui.groupAtom.setChecked(configParser.get("atomEnabled"))
        # firefox
        self.ui.firefox_line_light.setText(configParser.get("firefoxLight_Theme"))
        self.ui.firefox_line_dark.setText(configParser.get("firefoxDark_Theme"))
        self.ui.groupFirefox.setChecked(configParser.get("firefoxEnabled"))

    def open_wallpaper_light(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Light", "")
        subprocess.run(["notify-send", "Light Wallpaper set"])
        configParser.update("wallpaperLight_Theme", file_name)

    def open_wallpaper_dark(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Wallpaper Dark", "")
        subprocess.run(["notify-send", "Dark Wallpaper set"])
        configParser.update("wallpaperDark_Theme", file_name)

    def get_kde_themes(self):
        """
        Sends the kde themes to the ui.
        """
        if configParser.get("desktop") == "kde":
            if (self.ui.kde_combo_light.count() == 0 and
                self.ui.kde_combo_dark.count() == 0):
                kde_themes = self.get_kde_theme_names()

                for name, theme in kde_themes.items():
                    self.ui.kde_combo_light.addItem(name)
                    self.ui.kde_combo_dark.addItem(name)
        else:
            self.ui.groupKde.setChecked(False)
            configParser.update("kdeEnabled", False)

    def get_kde_theme_names(self):
        """
        Returns a map with translations for kde theme names.
        """

        # aliases for path to use later on
        user = pwd.getpwuid(os.getuid())[0]
        path = "/home/" + user + "/.local/share/plasma/look-and-feel/"

        # asks the system what themes are available
        long_names = subprocess.check_output(
            ["lookandfeeltool", "-l"], universal_newlines=True)
        long_names = long_names.splitlines()

        themes = {}

        # get the actual name
        for long in long_names:
            # trying to get the Desktop file
            try:
                # load the name from the metadata.desktop file
                with open('/usr/share/plasma/look-and-feel/{long}/metadata.desktop'.format(**locals()), 'r') as file:
                    # search for the name
                    for line in file:
                        if 'Name=' in line:
                            name: str = ''
                            write: bool = False
                            for letter in line:
                                if letter == '\n':
                                    write = False
                                if write:
                                    name += letter
                                if letter == '=':
                                    write = True
                            themes[name] = long
                            break
            except:
                # check the next path if the themes exist there
                try:
                    # load the name from the metadata.desktop file
                    with open('{path}{long}/metadata.desktop'.format(**locals()), 'r') as file:
                        # search for the name
                        for line in file:
                            if 'Name=' in line:
                                name: str = ''
                                write: bool = False
                                for letter in line:
                                    if letter == '\n':
                                        write = False
                                    if write:
                                        name += letter
                                    if letter == '=':
                                        write = True
                                themes[name] = long
                                break
                        # if no file exist lets just use the long name
                except:
                    themes[long] = long

        return themes

    def get_kde_theme_long(self, short: str):
        """
        Translates short names to long names.
        :param short: short name
        :return: long name
        """
        if short == '' or short is None:
            return
        themes = self.get_kde_theme_names()
        return themes[short]

    def get_kde_theme_short(self, long: str):
        """
        Translates long names to short names.
        :param long: long name
        :return: short name
        """
        if long == '' or long is None:
            return
        themes = self.get_kde_theme_names()
        short_names = list(themes.keys())
        long_names = list(themes.values())
        return short_names[long_names.index(long)]

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yin & Yang")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # center itself
        self.center()
        # syncs the UI with the config
        self.sync_with_config()
        # connects all buttons to the correct routes
        self.register_handlers()

    def center(self):
        frame_gm = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def register_handlers(self):
        # connect the "light" button
        self.ui.buttonLight.clicked.connect(self.toggle_light)
        # connect the "dark" button
        self.ui.buttonDark.clicked.connect(self.toggle_dark)
        # connect the time change with the correct function
        self.ui.inTimeLight.timeChanged.connect(self.time_changed)
        self.ui.inTimeDark.timeChanged.connect(self.time_changed)
        # connect position
        self.ui.inLatitude.valueChanged.connect(self.latitude_changed)
        self.ui.inLongitude.valueChanged.connect(self.longitude_changed)
        # connect schedule and sunposition
        self.ui.buttonSchedule.toggled.connect(self.toggle_schedule_clicked)
        self.ui.buttonSun.toggled.connect(self.toggle_sun)
        self.ui.automatic.toggled.connect(self.toggle_automatic)
        self.ui.checkSound.clicked.connect(self.toggle_sound)
        # connect the settingsButton
        self.ui.buttonApplication.clicked.connect(self.open_settings)

    def sync_with_config(self):
        # set current version in statusbar
        self.ui.statusBar.showMessage("yin-yang: v" +
                                      str(configParser.get("version")))
        # set the correct mode
        if configParser.get("mode") == config.Modes.scheduled.value:
            self.ui.buttonSchedule.setChecked(True)
        elif configParser.get("mode") == config.Modes.followSun.value:
            self.ui.buttonSun.setChecked(True)
        else:
            self.ui.automatic.setChecked(False)

        # sets the correct time based on config
        self.set_correct_time()
        # set correct coordinates
        self.ui.inLatitude.setValue(float(configParser.get("latitude")))
        self.ui.inLongitude.setValue(float(configParser.get("longitude")))
        # enable the correct button based on config
        self.set_correct_buttons()
        # connect checkbox for sound with config
        self.ui.checkSound.setChecked(configParser.get("sound_Enabled"))

    def open_settings(self):
        self.secwindow = SettingsWindow()
        self.secwindow.setWindowTitle("Settings")
        self.secwindow.show()
        self.hide()

    def toggle_light(self):
        configParser.update("mode", config.Modes.manual.value)
        yin_yang.switch_to_light()
        self.sync_with_config()
        # experimental
        # self.restart()

    def toggle_dark(self):
        configParser.update("mode", config.Modes.manual.value)
        yin_yang.switch_to_dark()
        self.sync_with_config()
        # self.restart()

    def toggle_sound(self):
        configParser.update("sound_Enabled", self.ui.checkSound.isChecked())

    # no needed since QT is now used system wise instead of python wise
    def restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def set_correct_time(self):
        d_hour = configParser.get("switch_To_Dark").split(":")[0]
        d_minute = configParser.get("switch_To_Dark").split(":")[1]
        l_hour = configParser.get("switch_To_Light").split(":")[0]
        l_minute = configParser.get("switch_To_Light").split(":")[1]

        # giving the time widget the values of the config
        dark_time = QTime(int(d_hour), int(d_minute))
        light_time = QTime(int(l_hour), int(l_minute))
        self.ui.inTimeDark.setTime(dark_time)
        self.ui.inTimeLight.setTime(light_time)

    def set_correct_buttons(self):
        if configParser.get("dark_mode"):
            self.ui.buttonLight.setEnabled(True)
            self.ui.buttonDark.setEnabled(False)
        else:
            self.ui.buttonLight.setEnabled(False)
            self.ui.buttonDark.setEnabled(True)

    def time_changed(self):
        # update config if time has changed
        l_hour, l_minute = str(self.ui.inTimeLight.time().hour()), str(
            self.ui.inTimeLight.time().minute())
        d_hour, d_minute = str(self.ui.inTimeDark.time().hour()), str(
            self.ui.inTimeDark.time().minute())
        configParser.update("switch_To_Light", l_hour + ":" + l_minute)
        configParser.update("switch_To_Dark", d_hour + ":" + d_minute)

    def toggle_schedule_clicked(self):
        configParser.update("mode", config.Modes.scheduled.value)

    def toggle_sun(self):
        configParser.update("mode", config.Modes.followSun.value)

    def toggle_automatic(self, checked):
        if checked:
            if self.ui.buttonSun.isChecked():
                configParser.update("mode", config.Modes.followSun.value)
            elif self.ui.buttonSchedule.isChecked():
                configParser.update("mode", config.Modes.scheduled.value)
        else:
            configParser.update("mode", config.Modes.manual.value)

    def latitude_changed(self, latitude):
        configParser.update("latitude", latitude)

    def longitude_changed(self, longitude):
        configParser.update("longitude", longitude)
