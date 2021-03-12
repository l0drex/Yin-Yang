# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../designer/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.setEnabled(True)
        main_window.resize(391, 633)
        main_window.setMinimumSize(QtCore.QSize(377, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_widget_layout.setContentsMargins(11, 11, 11, 11)
        self.central_widget_layout.setSpacing(6)
        self.central_widget_layout.setObjectName("central_widget_layout")
        self.logo_layout = QtWidgets.QHBoxLayout()
        self.logo_layout.setSpacing(6)
        self.logo_layout.setObjectName("logo_layout")
        self.logo = QtWidgets.QLabel(self.central_widget)
        self.logo.setPixmap(QtGui.QPixmap(":/icons/Logo"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.logo_layout.addWidget(self.logo, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.central_widget_layout.addLayout(self.logo_layout)
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setMinimumSize(QtCore.QSize(368, 0))
        self.tab_widget.setObjectName("tab_widget")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.settings_layout = QtWidgets.QVBoxLayout(self.settings)
        self.settings_layout.setContentsMargins(11, 11, 11, 11)
        self.settings_layout.setSpacing(6)
        self.settings_layout.setObjectName("settings_layout")
        self.btn_enable = QtWidgets.QCheckBox(self.settings)
        self.btn_enable.setChecked(True)
        self.btn_enable.setObjectName("btn_enable")
        self.settings_layout.addWidget(self.btn_enable)
        self.schedule_settings = QtWidgets.QWidget(self.settings)
        self.schedule_settings.setObjectName("schedule_settings")
        self.schedule_settings_layout = QtWidgets.QVBoxLayout(self.schedule_settings)
        self.schedule_settings_layout.setContentsMargins(11, 11, 11, 11)
        self.schedule_settings_layout.setSpacing(6)
        self.schedule_settings_layout.setObjectName("schedule_settings_layout")
        self.line_top = QtWidgets.QFrame(self.schedule_settings)
        self.line_top.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_top.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_top.setObjectName("line_top")
        self.schedule_settings_layout.addWidget(self.line_top)
        self.btn_schedule = QtWidgets.QRadioButton(self.schedule_settings)
        self.btn_schedule.setChecked(True)
        self.btn_schedule.setObjectName("btn_schedule")
        self.schedule_settings_layout.addWidget(self.btn_schedule)
        self.btn_sun = QtWidgets.QRadioButton(self.schedule_settings)
        self.btn_sun.setObjectName("btn_sun")
        self.schedule_settings_layout.addWidget(self.btn_sun)
        self.time = QtWidgets.QFrame(self.schedule_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setObjectName("time")
        self.time_layout = QtWidgets.QFormLayout(self.time)
        self.time_layout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.time_layout.setContentsMargins(37, 11, 11, 11)
        self.time_layout.setSpacing(6)
        self.time_layout.setObjectName("time_layout")
        self.label_light = QtWidgets.QLabel(self.time)
        self.label_light.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_light.setObjectName("label_light")
        self.time_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_light)
        self.inp_time_light = QtWidgets.QTimeEdit(self.time)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inp_time_light.sizePolicy().hasHeightForWidth())
        self.inp_time_light.setSizePolicy(sizePolicy)
        self.inp_time_light.setMinimumSize(QtCore.QSize(88, 0))
        self.inp_time_light.setTime(QtCore.QTime(8, 0, 0))
        self.inp_time_light.setObjectName("inp_time_light")
        self.time_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inp_time_light)
        self.label_dark = QtWidgets.QLabel(self.time)
        self.label_dark.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_dark.setObjectName("label_dark")
        self.time_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_dark)
        self.inp_time_dark = QtWidgets.QTimeEdit(self.time)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inp_time_dark.sizePolicy().hasHeightForWidth())
        self.inp_time_dark.setSizePolicy(sizePolicy)
        self.inp_time_dark.setMinimumSize(QtCore.QSize(88, 0))
        self.inp_time_dark.setTime(QtCore.QTime(20, 0, 0))
        self.inp_time_dark.setObjectName("inp_time_dark")
        self.time_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inp_time_dark)
        self.schedule_settings_layout.addWidget(self.time)
        self.location = QtWidgets.QFrame(self.schedule_settings)
        self.location.setObjectName("location")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.location)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.location_input = QtWidgets.QWidget(self.location)
        self.location_input.setObjectName("location_input")
        self.formLayout = QtWidgets.QFormLayout(self.location_input)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label_longitude = QtWidgets.QLabel(self.location_input)
        self.label_longitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_longitude.setObjectName("label_longitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_longitude)
        self.inp_longitude = QtWidgets.QDoubleSpinBox(self.location_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inp_longitude.sizePolicy().hasHeightForWidth())
        self.inp_longitude.setSizePolicy(sizePolicy)
        self.inp_longitude.setMinimumSize(QtCore.QSize(88, 0))
        self.inp_longitude.setMinimum(-180.0)
        self.inp_longitude.setMaximum(180.0)
        self.inp_longitude.setObjectName("inp_longitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inp_longitude)
        self.label_latitude = QtWidgets.QLabel(self.location_input)
        self.label_latitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_latitude.setObjectName("label_latitude")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_latitude)
        self.inp_latitude = QtWidgets.QDoubleSpinBox(self.location_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inp_latitude.sizePolicy().hasHeightForWidth())
        self.inp_latitude.setSizePolicy(sizePolicy)
        self.inp_latitude.setMinimumSize(QtCore.QSize(88, 0))
        self.inp_latitude.setMinimum(-90.0)
        self.inp_latitude.setMaximum(90.0)
        self.inp_latitude.setObjectName("inp_latitude")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inp_latitude)
        self.verticalLayout.addWidget(self.location_input)
        self.btn_location = QtWidgets.QCheckBox(self.location)
        self.btn_location.setObjectName("btn_location")
        self.verticalLayout.addWidget(self.btn_location)
        self.schedule_settings_layout.addWidget(self.location)
        self.line_bottom = QtWidgets.QFrame(self.schedule_settings)
        self.line_bottom.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_bottom.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_bottom.setObjectName("line_bottom")
        self.schedule_settings_layout.addWidget(self.line_bottom)
        self.settings_layout.addWidget(self.schedule_settings)
        self.toggle_sound = QtWidgets.QCheckBox(self.settings)
        self.toggle_sound.setObjectName("toggle_sound")
        self.settings_layout.addWidget(self.toggle_sound)
        self.toggle_notification = QtWidgets.QCheckBox(self.settings)
        self.toggle_notification.setObjectName("toggle_notification")
        self.settings_layout.addWidget(self.toggle_notification)
        self.label_active = QtWidgets.QLabel(self.settings)
        self.label_active.setObjectName("label_active")
        self.settings_layout.addWidget(self.label_active)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.settings_layout.addItem(spacerItem)
        self.tab_widget.addTab(self.settings, "")
        self.plugins = QtWidgets.QWidget()
        self.plugins.setObjectName("plugins")
        self.plugins_layout = QtWidgets.QVBoxLayout(self.plugins)
        self.plugins_layout.setContentsMargins(11, 11, 11, 11)
        self.plugins_layout.setSpacing(6)
        self.plugins_layout.setObjectName("plugins_layout")
        self.plugins_scroll = QtWidgets.QScrollArea(self.plugins)
        self.plugins_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plugins_scroll.setWidgetResizable(True)
        self.plugins_scroll.setObjectName("plugins_scroll")
        self.plugins_scroll_content = QtWidgets.QWidget()
        self.plugins_scroll_content.setGeometry(QtCore.QRect(0, 0, 348, 387))
        self.plugins_scroll_content.setObjectName("plugins_scroll_content")
        self.plugins_scroll_content_layout = QtWidgets.QVBoxLayout(self.plugins_scroll_content)
        self.plugins_scroll_content_layout.setContentsMargins(11, 11, 11, 11)
        self.plugins_scroll_content_layout.setSpacing(6)
        self.plugins_scroll_content_layout.setObjectName("plugins_scroll_content_layout")
        self.plugins_scroll.setWidget(self.plugins_scroll_content)
        self.plugins_layout.addWidget(self.plugins_scroll)
        self.tab_widget.addTab(self.plugins, "")
        self.central_widget_layout.addWidget(self.tab_widget)
        self.btn_box = QtWidgets.QDialogButtonBox(self.central_widget)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.btn_box.setObjectName("btn_box")
        self.central_widget_layout.addWidget(self.btn_box)
        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)

        self.retranslateUi(main_window)
        self.tab_widget.setCurrentIndex(0)
        self.btn_sun.toggled['bool'].connect(self.location.setVisible)
        self.btn_schedule.toggled['bool'].connect(self.time.setVisible)
        self.btn_enable.toggled['bool'].connect(self.schedule_settings.setVisible)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Yin & Yang"))
        self.btn_enable.setText(_translate("main_window", "Automatic theme switching"))
        self.btn_schedule.setText(_translate("main_window", "Custom Schedule"))
        self.btn_sun.setText(_translate("main_window", "Sunset to Sunrise"))
        self.label_light.setText(_translate("main_window", "Light:"))
        self.inp_time_light.setDisplayFormat(_translate("main_window", "HH:mm"))
        self.label_dark.setText(_translate("main_window", "Dark:"))
        self.inp_time_dark.setDisplayFormat(_translate("main_window", "HH:mm"))
        self.label_longitude.setText(_translate("main_window", "Longitude:"))
        self.inp_longitude.setSuffix(_translate("main_window", "°"))
        self.label_latitude.setText(_translate("main_window", "Latitude:"))
        self.inp_latitude.setSuffix(_translate("main_window", "°"))
        self.btn_location.setText(_translate("main_window", "update automatically"))
        self.toggle_sound.setText(_translate("main_window", "Make a sound when switching the theme"))
        self.toggle_notification.setText(_translate("main_window", "Send a notification"))
        self.label_active.setText(_translate("main_window", "Darkmode will be active between"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.settings), _translate("main_window", "Settings"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.plugins), _translate("main_window", "Plugins"))
import yin_yang.ui.resources_rc
