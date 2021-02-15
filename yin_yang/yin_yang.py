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

import threading
import time

from yin_yang.config import config, PLUGINS, Modes
from yin_yang.checker import Checker


def set_mode(dark: bool):
    print(f'Switching to {"dark" if dark else "light"} mode.')

    config.update('dark_mode', dark)
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)
    config.write()


class Daemon(threading.Thread):
    checker: Checker
    terminate = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.checker = Checker(config.get('mode'))

    def run(self):
        while True:
            if self.terminate or config.get('mode') == Modes.manual.value:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            dark_mode = self.checker.should_be_dark()
            if config.get('dark_mode') != dark_mode:
                set_mode(dark_mode)

            time.sleep(60)


def start_daemon():
    daemon = Daemon(1)
    daemon.start()
