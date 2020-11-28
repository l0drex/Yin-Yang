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

from src.config import config, PLUGINS, Modes


dark_mode: bool = config.get('dark_mode')


def set_mode(dark: bool):
    global dark_mode

    if dark == dark_mode:
        return

    dark_mode = dark
    config.update('dark_mode', dark)
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
            if self.terminate:
                config.update("running", False)
                config.write()
                break

            if config.get('mode') == Modes.manual.value:
                config.update("running", False)
                config.write()
                break

            # check if dark mode should be enabled and switch if necessary
            set_mode(should_be_dark())

            time.sleep(30)


def start_daemon():
    daemon = Daemon(1)
    daemon.start()


def should_be_dark():
    """
    Determines whether dark mode should be enabled or not
    """

    d_hour = int(config.get("switch_To_Dark").split(":")[0])
    d_minute = int(config.get("switch_To_Dark").split(":")[1])
    l_hour = int(config.get("switch_To_Light").split(":")[0])
    l_minute = int(config.get("switch_To_Light").split(":")[1])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    if l_hour <= hour < d_hour:
        return hour == l_hour and minute <= l_minute
    else:
        return not (hour == d_hour and minute <= d_minute)


def toggle_theme():
    """Switch themes"""
    set_mode(not config.get('dark_mode'))
