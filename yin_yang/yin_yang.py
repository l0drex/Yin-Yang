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

from yin_yang.checker import Checker
from yin_yang.config import config, PLUGINS

logger = logging.getLogger(__name__)


class Setter:
    dark_mode: bool = config.get('dark_mode')
    checker: Checker

    def __init__(self):
        self.checker = Checker(config.get('mode'))

    def set_mode(self, dark: bool):
        if dark == self.dark_mode:
            return

        logger.info(f'Switching to {"dark" if dark else "light"} mode.')
        config.update('dark_mode', dark)
        self.dark_mode = config.get('dark_mode')
        for p in PLUGINS:
            if config.get('enabled', plugin=p.name):
                p.set_mode(dark)
        config.write()

    def toggle_theme(self):
        """Switch themes"""
        self.set_mode(self.checker.should_be_dark())
