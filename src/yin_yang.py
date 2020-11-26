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
import os
import pwd
import threading
import time

from src import config

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/" + user + "/.config/"

configParser = config.ConfigParser(-1)
plugins = config.PLUGINS

terminate = False


class Switch(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def set_mode(self, dark: bool):
        for p in plugins:
            p.set_mode(dark)


class Daemon(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        while True:

            if terminate:
                configParser.update("running", False)
                break

            if not config.get('mode') == config.Modes.scheduled.value:
                configParser.update("running", False)
                break

            if should_be_dark():
                if configParser.get("dark_mode"):
                    time.sleep(30)
                    continue
                else:
                    switch_to_light()
            else:
                if not configParser.get("dark_mode"):
                    time.sleep(30)
                    continue
                else:
                    switch_to_dark()

            time.sleep(30)


def switch_to_light():
    yang = Yang(1)
    yang.start()
    configParser.update("dark_mode", False)
    yang.join()


def switch_to_dark():
    yin = Yin(2)
    yin.start()
    configParser.update("dark_mode", True)
    yin.join()


def start_daemon():
    daemon = Daemon(3)
    daemon.start()


def should_be_dark():
    # desc: return if the Theme should be light
    # returns: True if it should be light
    # returns: False if the theme should be dark

    d_hour = int(configParser.get("switch_To_Dark").split(":")[0])
    d_minute = int(configParser.get("switch_To_Dark").split(":")[1])
    l_hour = int(configParser.get("switch_To_Light").split(":")[0])
    l_minute = int(configParser.get("switch_To_Light").split(":")[1])
    hour = datetime.datetime.now().time().hour
    minute = datetime.datetime.now().time().minute

    if hour >= l_hour and hour < d_hour:
        return hour == l_hour and minute <= l_minute
    else:
        return not (hour == d_hour and minute <= d_minute)


def toggle_theme():
    """Switch themes"""
    if configParser.get("dark_mode"):
        switch_to_dark()
    else:
        switch_to_light()
