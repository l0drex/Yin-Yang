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
import threading
import time

from yin_yang.config import config, PLUGINS, Modes
from yin_yang.checker import Checker
from yin_yang.listener import Listener

logger = logging.getLogger(__name__)


class Setter:
    dark_mode: bool
    checker: Checker

    def __init__(self):
        self.checker = Checker(config.get('mode'))
        self.dark_mode = config.get('dark_mode')

    def set_mode(self, dark: bool):
        if dark == self.dark_mode:
            return

        logger.info(f'Switching to {"dark" if dark else "light"} mode.')
        self.dark_mode = config.update('dark_mode', dark)
        for p in PLUGINS:
            if config.get('enabled', plugin=p.name):
                p.set_mode(dark)
        config.write()

    def toggle_theme(self):
        """Switch themes"""
        self.set_mode(self.checker.should_be_dark())


class Daemon(threading.Thread):
    terminate = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.setter = Setter()
        self.name = 'Yin-Yang'

def run():
    listener = Listener('native')
    listener.run()
