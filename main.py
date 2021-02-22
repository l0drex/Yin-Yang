#!/bin/python
import logging
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


def main(arguments):
    config.debugging = arguments.debugging

    if arguments.toggle:
        setter = Setter()
        setter.toggle_theme()
    else:
        # load GUI to apply settings or set theme manually
        app = QtWidgets.QApplication(sys.argv)
        window = gui.MainWindow()
        window.show()
        app.exec_()


if __name__ == "__main__":
    args = parser.parse_args()

    if args.debugging:
        print('Debug mode enabled.')
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
    else:
        # logger to see what happens when application is running in background
        logging.basicConfig(filename='./yin_yang.log', level=logging.WARNING,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
    logger = logging.getLogger(__name__)

    main(args)
