#!/bin/python
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from yin_yang import yin_yang
from yin_yang.ui import gui
from yin_yang.config import Modes, config
from yin_yang.yin_yang import Setter


# using ArgumentParser for parsing arguments
parser = ArgumentParser()
parser.add_argument("-t", "--toggle",
                    help="toggles Yin-Yang",
                    action="store_true")
parser.add_argument("-s", "--schedule",
                    help="schedule theme toggle, starts daemon in bg",
                    action="store_true")
parser.add_argument('-d', '--debugging',
                    help='enables debugging mode',
                    action='store_true')

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def main(arguments):
    config.debugging = arguments.debugging

    # set settings via terminal
    if arguments.schedule:
        mode = config.get("mode")
        if mode == Modes.manual.value:
            print("looks like you did not specified a time")
            print("You can use the gui with yin-yang -gui")
            print("Or edit the config found in ~/.config/yin_yang/yin_yang.json")
            print("You need to set schedule to True and edit the time to toggles")
        else:
            print(f"Using mode {mode}")
    elif arguments.toggle:
        # toggle theme manually
        config.update("mode", Modes.manual.value)
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
        logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.WARNING,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')

    logger = logging.getLogger(__name__)

    main(args)
    if not config.debugging and config.get("mode") != Modes.manual.value:
        config.update("running", False)
        logger.info('Demon started')
        yin_yang.start_daemon()
