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

import dbus
from dbus.mainloop.glib import DBusGMainLoop

from yin_yang.config import config, PLUGINS
from yin_yang.checker import Checker, ManualMode

logger = logging.getLogger(__name__)


def handle_time_change(*args):
    if 'DayTime' in args[1]:
        dark_mode: bool = bool(args[1]['DayTime'])
        set_mode(dark_mode)


class Listener:
    def __init__(self, listener):
        if listener == 'native':
            self._mode = InternalMainLoop(Checker(config.get('mode')))
        #elif (listener == 'clight'):
            #self._mode = Clight()
        else:
            raise ValueError('Unexpected value for listener!')

    def run(self):
        self._mode.run()


class Mode(ABC):
    terminate = False

    def __init__(self):
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError('Method is not implemented.')


class InternalMainLoop(Mode):
    def __init__(self, checker: Checker):
        super(InternalMainLoop, self).__init__()
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

            set_mode(self._checker.should_be_dark())
            time.sleep(60)


class Clight(Mode):
    # source: https://github.com/FedeDP/Clight/wiki/DE-Automation

    def run(self):
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        # noinspection SpellCheckingInspection
        bus.add_signal_receiver(
            handle_time_change,
            'PropertiesChanged',
            'org.freedesktop.DBus.Properties',
            path='/org/clight/clight'
        )


def set_mode(dark: bool):
    if dark == config.get('dark_mode'):
        return

    logger.info(f'Switching to {"dark" if dark else "light"} mode.')
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)

    config.update('dark_mode', dark)
    config.write()


def run():
    listener = Listener(config.get('listener'))
    listener.run()
