#!/bin/python


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
import subprocess
import sys
import threading
import time

from src import config
from src.plugins import kde, gtkkde, wallpaper, vscode, atom, gtk, firefox, gnome, kvantum

# aliases for path to use later on
user = pwd.getpwuid(os.getuid())[0]
path = "/home/" + user + "/.config/"

configParser = config.ConfigParser(-1)

terminate = False


class Yang(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        if configParser.get("Enabled", plugin="code"):
            vscode.switch_to_light()
        if configParser.get("Enabled", plugin="atom"):
            atom.switch_to_light()
        if configParser.get("Enabled", plugin="kde"):
            kde.switch_to_light()
        if configParser.get("Enabled", plugin="wallpaper"):
            wallpaper.switch_to_light()
        # kde support
        if configParser.get("Enabled", plugin="gtk") and config.get("desktop") == "kde":
            gtkkde.switch_to_light()
        # gnome and budgie support
        if configParser.get("Enabled", plugin="gtk") and config.get("desktop") == "gtk":
            gtk.switch_to_light()
        # gnome-shell
        if configParser.get("Enabled", plugin="gnome"):
            gnome.switch_to_light()
        # firefox support
        if configParser.get("Enabled", plugin="firefox"):
            firefox.switch_to_light()
        # kvantum support
        if configParser.get("Enabled", plugin="kvantum"):
            kvantum.switch_to_light()
        play_sound("./assets/light.wav")


class Yin(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        if configParser.get("Enabled", plugin="code"):
            vscode.switch_to_dark()
        if configParser.get("Enabled", plugin="atom"):
            atom.switch_to_dark()
        if configParser.get("Enabled", "kde"):
            kde.switch_to_dark()
        if configParser.get("Enabled", plugin="wallpaper"):
            wallpaper.switch_to_dark()
        # kde support
        if configParser.get("Enabled", plugin="gtk") and config.get("desktop") == "kde":
            gtkkde.switch_to_dark()
        # gnome and budgie support
        if configParser.get("Enabled", plugin="gtk") and config.get("desktop") == "gtk":
            gtk.switch_to_dark()
        # gnome-shell
        if configParser.get("Enabled", plugin="gnome"):
            gnome.switch_to_dark()
        # firefox support
        if configParser.get("Enabled", plugin="firefox"):
            firefox.switch_to_dark()
        # kvantum support
        if configParser.get("Enabled", plugin="kvantum"):
            kvantum.switch_to_dark()
        play_sound("./assets/dark.wav")


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

            if should_be_light():
                if not configParser.get("dark_mode"):
                    time.sleep(30)
                    continue
                else:
                    switch_to_light()
            else:
                if configParser.get("dark_mode"):
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


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def play_sound(sound):
    """ Description - only works with pulseaudio.
    :type sound: String (Path)
    :param sound: Sound path to be played audio file from
    :rtype: I hope you will hear your Sound ;)
    """

    if configParser.get("sound_Enabled"):
        subprocess.run(["paplay", resource_path(sound)])


def should_be_light():
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
        return not (hour == l_hour and minute <= l_minute)
    else:
        return hour == d_hour and minute <= d_minute


def toggle_theme():
    """Switch themes"""
    if configParser.get("dark_mode"):
        switch_to_dark()
    else:
        switch_to_light()
