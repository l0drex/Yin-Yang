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

import datetime
import threading
import time

from yin_yang.config import config, PLUGINS, Modes
from yin_yang.checker import Checker


checker: Checker = Checker(config.get('mode'))
dark_mode: bool = config.get('dark_mode')


def set_mode(dark: bool):
    global dark_mode

    if dark == dark_mode:
        return

    print(f'Switching to {"dark" if dark else "light"} mode.')
    config.update('dark_mode', dark)
    dark_mode = config.get('dark_mode')
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)
    config.write()


class Daemon(threading.Thread):
    terminate = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        while True:
            if self.terminate or config.get('mode') == Modes.manual.value:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            toggle_theme()

            time.sleep(60)


def start_daemon():
    daemon = Daemon(1)
    daemon.start()


def toggle_theme():
    """Switch themes"""
    set_mode(checker.should_be_dark())
