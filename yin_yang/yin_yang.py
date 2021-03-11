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
from datetime import datetime

from yin_yang.config import config, PLUGINS

logger = logging.getLogger(__name__)


def handle_time_change(*args):
    if 'DayTime' in args[1]:
        dark_mode: bool = bool(args[1]['DayTime'])
        set_mode(dark_mode)


class Listener:
    def __init__(self, listener):
        if listener == 'native':
            self._mode = Native()
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


def should_be_dark(time_current: time, time_light: time, time_dark: time) -> bool:
    """Compares two times with current time"""

    if time_light < time_dark:
        return not (time_light <= time_current < time_dark)
    else:
        return time_dark <= time_current < time_light


class Native(Mode):
    def run(self):
        while True:
            if self.terminate:
                config.running = False
                config.write()
                break

            time_light, time_dark = config.times
            set_mode(should_be_dark(datetime.now().time(), time_light, time_dark))
            time.sleep(60)


def set_mode(dark: bool):
    if dark == config.dark_mode:
        return

    logger.info(f'Switching to {"dark" if dark else "light"} mode.')
    for p in PLUGINS:
        if config.get(p.name, 'enabled'):
            p.set_mode(dark)

    config.dark_mode = dark
    config.write()


def run():
    listener = Listener(config.listener)
    listener.run()
