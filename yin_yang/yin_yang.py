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
from yin_yang.listener import Listener


def set_mode(dark: bool):
    print(f'Switching to {"dark" if dark else "light"} mode.')

    config.update('dark_mode', dark)
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)
    config.write()


def run():
    listener = Listener('native')
    listener.run()
