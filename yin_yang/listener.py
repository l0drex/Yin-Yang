#!/usr/bin/env python

import dbus
import subprocess
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

# source: https://github.com/FedeDP/Clight/wiki/DE-Automation
old_time = -1  # 0 -> day, 1 -> night


def handle_time_change(*args):
    global old_time
    if 'DayTime' in args[1] and old_time != args[1]['DayTime']:
        if args[1]['DayTime'] == 1:
            # noinspection SpellCheckingInspection
            subprocess.Popen(["lookandfeeltool", "-a", "org.kde.breezedark.desktop"])
        elif args[1]['DayTime'] == 0:
            # noinspection SpellCheckingInspection
            subprocess.Popen(["lookandfeeltool", "-a", "org.kde.breeze.desktop"])
        old_time = args[1]['DayTime']


DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
# noinspection SpellCheckingInspection
bus.add_signal_receiver(
    handle_time_change,
    'PropertiesChanged',
    'org.freedesktop.DBus.Properties',
    path='/org/clight/clight'
)

loop = GLib.MainLoop().run()
