#!/usr/bin/env python
import locale
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QTranslator

from yin_yang import yin_yang
from yin_yang.ui import config_window
from yin_yang.config import Modes, config


# using ArgumentParser for parsing arguments
from yin_yang.yin_yang import set_mode

logger = logging.getLogger(__name__)

parser = ArgumentParser()
parser.add_argument('-t', '--toggle',
                    help='toggles Yin-Yang',
                    action='store_true')
parser.add_argument('-s', '--schedule',
                    help='schedule theme toggle, starts daemon in bg',
                    action='store_true')

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def main():
    arguments = parser.parse_args()
    # set settings via terminal
    if arguments.schedule:
        mode = config.mode
        if mode == Modes.manual:
            print('Mode is set to manual. Therefore automatic theme changing is disabled.'
                  'To enable, start yin yang without arguments to open the gui '
                  'or edit to file ~/.config/yin_yang/yin_yang.json')
            return
        elif not config.running:
            logger.info(f'Starting in mode {mode.name}')
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

        # load translation
        try:
            translator = QTranslator()
            lang = locale.getdefaultlocale()[0].split('_')[0]
            logger.debug(f'Using language {lang}')
            if not translator.load(':/language/yin_yang.' + lang + '.qm'):
                logger.warning('Error while loading translation file!')
            app.installTranslator(translator)
        except Exception as e:
            logger.error(str(e))
            print('Error while loading translation. Using default language.')

        window = config_window.MainWindow()
        window.show()
        app.exec_()


if __name__ == '__main__':
    if __debug__:
        # noinspection SpellCheckingInspection
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')
    else:
        # logger to see what happens when application is running in background
        # noinspection SpellCheckingInspection
        logging.basicConfig(filename=str(Path.home()) + '/.local/share/yin_yang.log', level=logging.WARNING,
                            format='%(asctime)s %(levelname)s - %(name)s: %(message)s')

    main()
