import sys
from argparse import ArgumentParser
from src import yin_yang
from src.config import config, Modes
from src import gui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)

config.debugging = False


def main():
    # using ArgumentParser for parsing arguments
    parser = ArgumentParser()
    parser.add_argument("-t", "--toggle",
                        help="toggles Yin-Yang",
                        action="store_true")
    parser.add_argument("-s", "--schedule",
                        help="schedule theme toggle, starts daemon in bg",
                        action="store_true")
    args = parser.parse_args()

    # checks whether $ yin-yang is ran without args
    if len(sys.argv) == 1 and not args.toggle:
        # load GUI to apply settings or set theme manually
        app = QtWidgets.QApplication(sys.argv)
        window = gui.MainWindow()
        window.show()
        app.exec_()
    else:
        # set settings via terminal
        if args.schedule:
            mode = config.get("mode")
            if mode == Modes.manual.value:
                print("looks like you did not specified a time")
                print("You can use the gui with yin-yang -gui")
                print("Or edit the config found in ~/.config/yin_yang/yin_yang.json")
                print("You need to set schedule to True and edit the time to toggles")
            else:
                print(f"Using mode {mode}")
        elif args.toggle:
            # toggle theme manually
            config.update("mode", Modes.manual.value)
            yin_yang.toggle_theme()


if __name__ == "__main__":
    main()
    if config.get("mode") != Modes.manual.value:
        config.update("running", False)
        print("START thread listener")
        yin_yang.start_daemon()
