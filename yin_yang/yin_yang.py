# noinspection SpellCheckingInspection
"""
title: yin_yang
description: yin_yang provides a easy way to toggle between light and dark
mode for your kde desktop. It also themes your vscode and
all other qt application with it.
author: daehruoydeef
date: 21.12.2018
license: MIT
"""
import logging
import time
from abc import ABC, abstractmethod

from yin_yang.config import config, PLUGINS
from yin_yang.checker import Checker, ManualMode

logger = logging.getLogger(__name__)


class Listener:
    def __init__(self, listener):
        if listener == 'native':
            self._mode = Native(config.get('mode'))
        elif listener == 'clight':
            self._mode = Clight()

    def run(self):
        self._mode.run()


class Mode(ABC):
    terminate = False

    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError('Method is not implemented.')


class Native(Mode):
    def __init__(self, checker: Checker):
        super(Native, self).__init__()
        if isinstance(checker, ManualMode):
            raise ValueError('No notifier needed if mode is manual!')
        else:
            self._checker = checker

    def run(self):
        while True:
            if self.terminate:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            dark_mode = self._checker.should_be_dark()
            if dark_mode != config.get('dark_mode'):
                set_mode(dark_mode)
                config.update('dark_mode', dark_mode)
            time.sleep(60)


class Clight(Mode):
    # source: https://github.com/FedeDP/Clight/wiki/DE-Automation

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
        dark_mode: bool = bool(args[1]['DayTime'])
        if 'DayTime' in args[1] and config.get('dark_mode') != dark_mode:
            set_mode(dark_mode)
            config.update('dark_mode', dark_mode)

    def run(self):
        GLib.MainLoop().run()


def set_mode(dark: bool):
    logger.info(f'Switching to {"dark" if dark else "light"} mode.')
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)
    config.write()


def run():
    listener = Listener('native')
    listener.run()
