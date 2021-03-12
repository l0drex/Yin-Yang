#!/usr/bin/env python

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from yin_yang import yin_yang
from yin_yang.ui import config_window
from yin_yang.config import Modes, config


# using ArgumentParser for parsing arguments
from yin_yang.yin_yang import set_mode

parser = ArgumentParser()
parser.add_argument('-t', '--toggle',
                    help='toggles Yin-Yang',
                    action='store_true')
parser.add_argument('-s', '--schedule',
                    help='schedule theme toggle, starts daemon in bg',
                    action='store_true')
parser.add_argument('-d', '--debugging',
                    help='enables debugging mode',
                    action='store_true')

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def main(arguments):
    # set settings via terminal
    if arguments.schedule:
        mode = config.mode
        if mode == Modes.manual:
            print('Mode is set to manual. Therefore automatic theme changing is disabled.'
                  'To enable, start yin yang without arguments to open the gui '
                  'or edit to file ~/.config/yin_yang/yin_yang.json')
            return
        elif not config.running:
            print(f'Starting in mode {mode.name}')
            time_light, time_dark = config.times
            print(f'Dark mode will be active between {time_dark} and {time_light}')
            yin_yang.run()
        else:
            raise ValueError('Yin Yang is already running')
    elif arguments.toggle:
        # toggle theme manually
        config.mode = Modes.manual
        set_mode(not config.dark_mode)
    else:
        # load GUI to apply settings or set theme manually
        app = QtWidgets.QApplication(sys.argv)
        window = config_window.MainWindow()
        window.show()
        app.exec_()


if __name__ == '__main__':
    args = parser.parse_args()

    if args.debugging:
        print('Debug mode enabled.')
        # noinspection SpellCheckingInspection
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
    else:
        # logger to see what happens when application is running in background
        # noinspection SpellCheckingInspection
        logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.WARNING,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')

    main(args)
