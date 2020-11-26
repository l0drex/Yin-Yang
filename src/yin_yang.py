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

from src import config


configParser = config.ConfigParser(-1)
plugins = config.PLUGINS


class Daemon(threading.Thread):
    terminate = False

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

        self.dark_mode: bool = configParser.get('dark_mode')

    def run(self):
        while True:
            if self.terminate:
                configParser.update("running", False)
                break

            if configParser.get('mode') == config.Modes.manual.value:
                configParser.update("running", False)
                break

            # check if dark mode should be enabled
            dark: bool = should_be_dark()

            # switch if necessary
            if dark != self.dark_mode:
                self.dark_mode = dark
                configParser.update('dark_mode', dark)
                for p in plugins:
                    p.set_mode(dark)

            time.sleep(30)


def start_daemon():
    daemon = Daemon(1)
    daemon.start()


def should_be_dark():
    """
    Determines whether dark mode should be enabled or not
    """

    d_hour = int(configParser.get("switch_To_Dark").split(":")[0])
    d_minute = int(configParser.get("switch_To_Dark").split(":")[1])
    l_hour = int(configParser.get("switch_To_Light").split(":")[0])
    l_minute = int(configParser.get("switch_To_Light").split(":")[1])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    if l_hour <= hour < d_hour:
        return hour == l_hour and minute <= l_minute
    else:
        return not (hour == d_hour and minute <= d_minute)


def toggle_theme():
    """Switch themes"""
    for p in plugins:
        p.set_mode(not configParser.get('dark_mode'))
