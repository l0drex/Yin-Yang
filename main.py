#!/bin/python

import sys
from argparse import ArgumentParser
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from yin_yang.ui import gui
from yin_yang.config import config
from yin_yang.yin_yang import Setter

# using ArgumentParser for parsing arguments
parser = ArgumentParser()
parser.add_argument("-t", "--toggle",
                    help="Changes to dark or light if needed",
                    action="store_true")
parser.add_argument('-d', '--debugging',
                    help='enables debugging mode',
                    action='store_true')

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def main():
    args = parser.parse_args()

    config.debugging = args.debugging

    if args.toggle:
        setter = Setter()
        setter.toggle_theme()
    else:
        # load GUI to apply settings or set theme manually
        app = QtWidgets.QApplication(sys.argv)
        window = gui.MainWindow()
        window.show()
        app.exec_()


if __name__ == "__main__":
    main()
