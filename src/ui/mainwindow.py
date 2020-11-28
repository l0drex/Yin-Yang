# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(433, 643)
        MainWindow.setMinimumSize(QtCore.QSize(377, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/yin-yang.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo = QtWidgets.QHBoxLayout()
        self.logo.setSpacing(6)
        self.logo.setObjectName("logo")
        self.imgLogo = QtWidgets.QLabel(self.centralWidget)
        self.imgLogo.setPixmap(QtGui.QPixmap(":/icons/assets/yin-yang.svg"))
        self.imgLogo.setScaledContents(True)
        self.imgLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLogo.setObjectName("imgLogo")
        self.logo.addWidget(self.imgLogo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.logo)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settings)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.buttonManual = QtWidgets.QRadioButton(self.settings)
        self.buttonManual.setChecked(True)
        self.buttonManual.setObjectName("buttonManual")
        self.verticalLayout_3.addWidget(self.buttonManual)
        self.buttonSchedule = QtWidgets.QRadioButton(self.settings)
        self.buttonSchedule.setChecked(False)
        self.buttonSchedule.setObjectName("buttonSchedule")
        self.verticalLayout_3.addWidget(self.buttonSchedule)
        self.time = QtWidgets.QFrame(self.settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setObjectName("time")
        self.formLayout = QtWidgets.QFormLayout(self.time)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setHorizontalSpacing(40)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.labelLight = QtWidgets.QLabel(self.time)
        self.labelLight.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLight.setObjectName("labelLight")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelLight)
        self.inTimeLight = QtWidgets.QTimeEdit(self.time)
        self.inTimeLight.setTime(QtCore.QTime(8, 0, 0))
        self.inTimeLight.setObjectName("inTimeLight")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inTimeLight)
        self.labelDark = QtWidgets.QLabel(self.time)
        self.labelDark.setObjectName("labelDark")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelDark)
        self.inTimeDark = QtWidgets.QTimeEdit(self.time)
        self.inTimeDark.setTime(QtCore.QTime(20, 0, 0))
        self.inTimeDark.setObjectName("inTimeDark")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inTimeDark)
        self.verticalLayout_3.addWidget(self.time)
        self.buttonSun = QtWidgets.QRadioButton(self.settings)
        self.buttonSun.setObjectName("buttonSun")
        self.verticalLayout_3.addWidget(self.buttonSun)
        self.location = QtWidgets.QFrame(self.settings)
        self.location.setEnabled(False)
        self.location.setObjectName("location")
        self.formLayout_2 = QtWidgets.QFormLayout(self.location)
        self.formLayout_2.setContentsMargins(11, 11, 11, 11)
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelLatitude = QtWidgets.QLabel(self.location)
        self.labelLatitude.setObjectName("labelLatitude")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelLatitude)
        self.labelLongitude = QtWidgets.QLabel(self.location)
        self.labelLongitude.setObjectName("labelLongitude")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelLongitude)
        self.inLatitude = QtWidgets.QDoubleSpinBox(self.location)
        self.inLatitude.setMinimum(-90.0)
        self.inLatitude.setMaximum(90.0)
        self.inLatitude.setObjectName("inLatitude")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inLatitude)
        self.inLongitude = QtWidgets.QDoubleSpinBox(self.location)
        self.inLongitude.setMinimum(-180.0)
        self.inLongitude.setMaximum(180.0)
        self.inLongitude.setObjectName("inLongitude")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inLongitude)
        self.buttonLocation = QtWidgets.QPushButton(self.location)
        self.buttonLocation.setObjectName("buttonLocation")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonLocation)
        self.verticalLayout_3.addWidget(self.location)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget.addTab(self.settings, "")
        self.plugins = QtWidgets.QWidget()
        self.plugins.setObjectName("plugins")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.plugins)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.toolBox = QtWidgets.QToolBox(self.plugins)
        self.toolBox.setObjectName("toolBox")
        self.system = QtWidgets.QWidget()
        self.system.setGeometry(QtCore.QRect(0, -149, 380, 468))
        self.system.setObjectName("system")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.system)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupKde = QtWidgets.QGroupBox(self.system)
        self.groupKde.setCheckable(True)
        self.groupKde.setObjectName("groupKde")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupKde)
        self.horizontalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.kde_light = QtWidgets.QComboBox(self.groupKde)
        self.kde_light.setObjectName("kde_light")
        self.horizontalLayout_9.addWidget(self.kde_light)
        self.kde_dark = QtWidgets.QComboBox(self.groupKde)
        self.kde_dark.setObjectName("kde_dark")
        self.horizontalLayout_9.addWidget(self.kde_dark)
        self.verticalLayout_5.addWidget(self.groupKde)
        self.groupGnome = QtWidgets.QGroupBox(self.system)
        self.groupGnome.setCheckable(True)
        self.groupGnome.setObjectName("groupGnome")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupGnome)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gnome_light = QtWidgets.QLineEdit(self.groupGnome)
        self.gnome_light.setObjectName("gnome_light")
        self.horizontalLayout_2.addWidget(self.gnome_light)
        self.gnome_dark = QtWidgets.QLineEdit(self.groupGnome)
        self.gnome_dark.setObjectName("gnome_dark")
        self.horizontalLayout_2.addWidget(self.gnome_dark)
        self.verticalLayout_5.addWidget(self.groupGnome)
        self.groupKvantum = QtWidgets.QGroupBox(self.system)
        self.groupKvantum.setCheckable(True)
        self.groupKvantum.setObjectName("groupKvantum")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupKvantum)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.kvantum_light = QtWidgets.QLineEdit(self.groupKvantum)
        self.kvantum_light.setText("")
        self.kvantum_light.setObjectName("kvantum_light")
        self.horizontalLayout_4.addWidget(self.kvantum_light)
        self.kvantum_dark = QtWidgets.QLineEdit(self.groupKvantum)
        self.kvantum_dark.setObjectName("kvantum_dark")
        self.horizontalLayout_4.addWidget(self.kvantum_dark)
        self.verticalLayout_5.addWidget(self.groupKvantum)
        self.groupGtk = QtWidgets.QGroupBox(self.system)
        self.groupGtk.setCheckable(True)
        self.groupGtk.setChecked(True)
        self.groupGtk.setObjectName("groupGtk")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupGtk)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gtk_light = QtWidgets.QLineEdit(self.groupGtk)
        self.gtk_light.setText("")
        self.gtk_light.setObjectName("gtk_light")
        self.horizontalLayout_5.addWidget(self.gtk_light)
        self.gtk_dark = QtWidgets.QLineEdit(self.groupGtk)
        self.gtk_dark.setText("")
        self.gtk_dark.setObjectName("gtk_dark")
        self.horizontalLayout_5.addWidget(self.gtk_dark)
        self.verticalLayout_5.addWidget(self.groupGtk)
        self.groupWallpaper = QtWidgets.QGroupBox(self.system)
        self.groupWallpaper.setCheckable(True)
        self.groupWallpaper.setObjectName("groupWallpaper")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupWallpaper)
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.wallpaper_light_group = QtWidgets.QWidget(self.groupWallpaper)
        self.wallpaper_light_group.setObjectName("wallpaper_light_group")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.wallpaper_light_group)
        self.verticalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.wallpaper_light = QtWidgets.QLineEdit(self.wallpaper_light_group)
        self.wallpaper_light.setText("")
        self.wallpaper_light.setObjectName("wallpaper_light")
        self.verticalLayout_9.addWidget(self.wallpaper_light)
        self.wallpaper_light_open = QtWidgets.QDialogButtonBox(self.wallpaper_light_group)
        self.wallpaper_light_open.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.wallpaper_light_open.setObjectName("wallpaper_light_open")
        self.verticalLayout_9.addWidget(self.wallpaper_light_open)
        self.horizontalLayout_7.addWidget(self.wallpaper_light_group)
        self.wallpaper_dark_group = QtWidgets.QWidget(self.groupWallpaper)
        self.wallpaper_dark_group.setObjectName("wallpaper_dark_group")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.wallpaper_dark_group)
        self.verticalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.wallpaper_dark = QtWidgets.QLineEdit(self.wallpaper_dark_group)
        self.wallpaper_dark.setObjectName("wallpaper_dark")
        self.verticalLayout_10.addWidget(self.wallpaper_dark)
        self.wallpaper_dark_open = QtWidgets.QDialogButtonBox(self.wallpaper_dark_group)
        self.wallpaper_dark_open.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.wallpaper_dark_open.setObjectName("wallpaper_dark_open")
        self.verticalLayout_10.addWidget(self.wallpaper_dark_open)
        self.horizontalLayout_7.addWidget(self.wallpaper_dark_group)
        self.verticalLayout_5.addWidget(self.groupWallpaper)
        self.toolBox.addItem(self.system, "")
        self.applications = QtWidgets.QWidget()
        self.applications.setGeometry(QtCore.QRect(0, 0, 401, 170))
        self.applications.setObjectName("applications")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.applications)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupVscode = QtWidgets.QGroupBox(self.applications)
        self.groupVscode.setCheckable(True)
        self.groupVscode.setObjectName("groupVscode")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupVscode)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.code_light = QtWidgets.QLineEdit(self.groupVscode)
        self.code_light.setObjectName("code_light")
        self.horizontalLayout.addWidget(self.code_light)
        self.code_dark = QtWidgets.QLineEdit(self.groupVscode)
        self.code_dark.setObjectName("code_dark")
        self.horizontalLayout.addWidget(self.code_dark)
        self.verticalLayout_6.addWidget(self.groupVscode)
        self.groupAtom = QtWidgets.QGroupBox(self.applications)
        self.groupAtom.setCheckable(True)
        self.groupAtom.setObjectName("groupAtom")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupAtom)
        self.horizontalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.atom_light = QtWidgets.QLineEdit(self.groupAtom)
        self.atom_light.setObjectName("atom_light")
        self.horizontalLayout_8.addWidget(self.atom_light)
        self.atom_dark = QtWidgets.QLineEdit(self.groupAtom)
        self.atom_dark.setObjectName("atom_dark")
        self.horizontalLayout_8.addWidget(self.atom_dark)
        self.verticalLayout_6.addWidget(self.groupAtom)
        self.toolBox.addItem(self.applications, "")
        self.other = QtWidgets.QWidget()
        self.other.setGeometry(QtCore.QRect(0, 0, 380, 212))
        self.other.setObjectName("other")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.other)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupSound = QtWidgets.QGroupBox(self.other)
        self.groupSound.setCheckable(True)
        self.groupSound.setObjectName("groupSound")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupSound)
        self.horizontalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.sound_light_group = QtWidgets.QWidget(self.groupSound)
        self.sound_light_group.setObjectName("sound_light_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sound_light_group)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sound_light = QtWidgets.QLineEdit(self.sound_light_group)
        self.sound_light.setObjectName("sound_light")
        self.verticalLayout.addWidget(self.sound_light)
        self.sound_light_open = QtWidgets.QDialogButtonBox(self.sound_light_group)
        self.sound_light_open.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.sound_light_open.setObjectName("sound_light_open")
        self.verticalLayout.addWidget(self.sound_light_open)
        self.horizontalLayout_10.addWidget(self.sound_light_group)
        self.sound_dark_group = QtWidgets.QWidget(self.groupSound)
        self.sound_dark_group.setObjectName("sound_dark_group")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.sound_dark_group)
        self.verticalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.sound_dark = QtWidgets.QLineEdit(self.sound_dark_group)
        self.sound_dark.setObjectName("sound_dark")
        self.verticalLayout_8.addWidget(self.sound_dark)
        self.sound_dark_open = QtWidgets.QDialogButtonBox(self.sound_dark_group)
        self.sound_dark_open.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.sound_dark_open.setObjectName("sound_dark_open")
        self.verticalLayout_8.addWidget(self.sound_dark_open)
        self.horizontalLayout_10.addWidget(self.sound_dark_group)
        self.verticalLayout_7.addWidget(self.groupSound)
        self.groupUsb = QtWidgets.QGroupBox(self.other)
        self.groupUsb.setCheckable(True)
        self.groupUsb.setObjectName("groupUsb")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupUsb)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.usb_light = QtWidgets.QCheckBox(self.groupUsb)
        self.usb_light.setObjectName("usb_light")
        self.horizontalLayout_3.addWidget(self.usb_light)
        self.usb_dark = QtWidgets.QCheckBox(self.groupUsb)
        self.usb_dark.setObjectName("usb_dark")
        self.horizontalLayout_3.addWidget(self.usb_dark)
        self.verticalLayout_7.addWidget(self.groupUsb)
        self.toolBox.addItem(self.other, "")
        self.verticalLayout_4.addWidget(self.toolBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.tabWidget.addTab(self.plugins, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Reset|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        self.buttonSchedule.toggled['bool'].connect(self.time.setEnabled)
        self.buttonSun.toggled['bool'].connect(self.location.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yin & Yang"))
        self.buttonManual.setText(_translate("MainWindow", "manual"))
        self.buttonSchedule.setText(_translate("MainWindow", "scheduled"))
        self.labelLight.setText(_translate("MainWindow", "Light:"))
        self.inTimeLight.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.labelDark.setText(_translate("MainWindow", "Dark:"))
        self.inTimeDark.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.buttonSun.setText(_translate("MainWindow", "set sunset and sunrise"))
        self.labelLatitude.setText(_translate("MainWindow", "Latitude:"))
        self.labelLongitude.setText(_translate("MainWindow", "Longitude:"))
        self.inLatitude.setSuffix(_translate("MainWindow", "°"))
        self.inLongitude.setSuffix(_translate("MainWindow", "°"))
        self.buttonLocation.setText(_translate("MainWindow", "Set current location"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Settings"))
        self.groupKde.setTitle(_translate("MainWindow", "KDE"))
        self.groupGnome.setTitle(_translate("MainWindow", "Gnome"))
        self.gnome_light.setPlaceholderText(_translate("MainWindow", "Light Theme"))
        self.gnome_dark.setPlaceholderText(_translate("MainWindow", "Dark Theme"))
        self.groupKvantum.setTitle(_translate("MainWindow", "Kvantum"))
        self.kvantum_light.setPlaceholderText(_translate("MainWindow", "Light Theme"))
        self.kvantum_dark.setPlaceholderText(_translate("MainWindow", "Dark Theme"))
        self.groupGtk.setTitle(_translate("MainWindow", "GTK"))
        self.gtk_light.setPlaceholderText(_translate("MainWindow", "Light Theme"))
        self.gtk_dark.setPlaceholderText(_translate("MainWindow", "Dark Theme"))
        self.groupWallpaper.setToolTip(_translate("MainWindow", "Change the wallpaper depending on the theme"))
        self.groupWallpaper.setTitle(_translate("MainWindow", "Wallpaper"))
        self.wallpaper_light.setPlaceholderText(_translate("MainWindow", "Light"))
        self.wallpaper_dark.setPlaceholderText(_translate("MainWindow", "Dark"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.system), _translate("MainWindow", "System"))
        self.groupVscode.setTitle(_translate("MainWindow", "VS Code"))
        self.code_light.setPlaceholderText(_translate("MainWindow", "Light Theme"))
        self.code_dark.setPlaceholderText(_translate("MainWindow", "Dark Theme"))
        self.groupAtom.setTitle(_translate("MainWindow", "Atom"))
        self.atom_light.setPlaceholderText(_translate("MainWindow", "Light Theme"))
        self.atom_dark.setPlaceholderText(_translate("MainWindow", "Dark Theme"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.applications), _translate("MainWindow", "Applications"))
        self.groupSound.setToolTip(_translate("MainWindow", "Make a sound when the theme is switched."))
        self.groupSound.setTitle(_translate("MainWindow", "Sound"))
        self.sound_light.setPlaceholderText(_translate("MainWindow", "Light Sound"))
        self.sound_dark.setPlaceholderText(_translate("MainWindow", "Dark Sound"))
        self.groupUsb.setToolTip(_translate("MainWindow", "Change the power state of a usb port. Useful when you have a light connected"))
        self.groupUsb.setTitle(_translate("MainWindow", "USB"))
        self.usb_light.setText(_translate("MainWindow", "power when light"))
        self.usb_dark.setText(_translate("MainWindow", "power when dark"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.other), _translate("MainWindow", "Miscellaneous"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plugins), _translate("MainWindow", "Plugins"))
import resources_rc
