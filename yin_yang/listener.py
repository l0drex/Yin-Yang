#!/usr/bin/python

import time
from abc import ABC, abstractmethod

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from yin_yang.checker import Checker
from yin_yang.config import config, Modes
from yin_yang.yin_yang import set_mode


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

    @abstractmethod
    def run(self):
        raise NotImplementedError('Method is not implemented.')


class Native(Mode):
    def __init__(self):
        super().__init__()
        self._checker = Checker(config.get('mode'))

    def run(self):
        while True:
            if self.terminate or config.get('mode') == Modes.manual.value:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            dark_mode = self._checker.should_be_dark()
            if config.get('dark_mode') != dark_mode:
                set_mode(dark_mode)

            time.sleep(60)


class Clight(Mode):
    # source: https://github.com/FedeDP/Clight/wiki/DE-Automation
    _old_time = -1  # 0 -> day, 1 -> night

    def __init__(self):
        super().__init__()
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
        if 'DayTime' in args[1] and self._old_time != args[1]['DayTime']:
            set_mode(bool(args[1]['DayTime']))
            self._old_time = args[1]['DayTime']

    def run(self):
        GLib.MainLoop().run()
