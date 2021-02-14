"""
title: yin_yang
description: yin_yang provides a easy way to toggle between light and dark
mode for your kde desktop. It also themes your vscode and
all other qt application with it.
author: daehruoydeef
date: 21.12.2018
license: MIT
"""

from yin_yang.config import config, PLUGINS, Modes
from yin_yang.toggle_checker.checker import Checker
from yin_yang.toggle_checker.manual import Manual
from yin_yang.toggle_checker.sun import Sun
from yin_yang.toggle_checker.time import Time


def get_checker():
    """Specify a mode in which the theme to be used is determined"""
    mode = config.get('mode')
    if mode == Modes.manual.value:
        return Manual()
    elif mode == Modes.scheduled.value:
        return Time()
    elif mode == Modes.followSun.value:
        return Sun()
    else:
        raise ValueError('Unknown mode specified!')


checker: Checker = get_checker()
dark_mode: bool = config.get('dark_mode')


def set_mode(dark: bool):
    global dark_mode

    if dark == dark_mode:
        print('No changes needed')
        return

    config.update('dark_mode', dark)
    dark_mode = config.get('dark_mode')
    for p in PLUGINS:
        if config.get('enabled', plugin=p.name):
            p.set_mode(dark)
    config.write()


def toggle_theme():
    """Switch themes"""
    set_mode(checker.should_be_dark())
