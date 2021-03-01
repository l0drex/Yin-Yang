#!/usr/bin/python

import time
from abc import ABC, abstractmethod

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from yin_yang.checker import Checker
from yin_yang.config import config, Modes
from yin_yang.yin_yang import Setter


class Listener:
    def __init__(self, listener):
        if listener == 'native':
            self._mode = Native()
        elif listener == 'clight':
            self._mode = Clight()

    def run(self):
        self._mode.run()


class Mode(ABC):
    terminate = False

    def __init__(self):
        self.setter = Setter()

    @abstractmethod
    def run(self):
        raise NotImplementedError('Method is not implemented.')


class Native(Mode):
    def __init__(self):
        super(Native, self).__init__()
        self.name = 'Yin-Yang'

    def run(self):
        while True:
            if self.terminate or config.get('mode') == Modes.manual.value:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            self.setter.toggle_theme()

            time.sleep(60)


class Clight(Mode):
    # source: https://github.com/FedeDP/Clight/wiki/DE-Automation

    def __init__(self):
        super().__init__()

        self._dark_mode_current: bool = config.get('dark_mode')  # 0 -> day, 1 -> night

        DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        # noinspection SpellCheckingInspection
        bus.add_signal_receiver(
            self.handle_time_change,
            'PropertiesChanged',
            'org.freedesktop.DBus.Properties',
            path='/org/clight/clight'
        )

    def handle_time_change(self, *args):
        dark_mode: bool = bool(args[1]['DayTime'])
        if 'DayTime' in args[1] and self._dark_mode_current != dark_mode:
            self.setter.toggle_theme()
            self._dark_mode_current = dark_mode

    def run(self):
        GLib.MainLoop().run()
