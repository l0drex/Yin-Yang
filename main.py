import sys
from argparse import ArgumentParser
from src import yin_yang
from src import config
from src import gui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

assembly_version = 2.2
configParser = config.ConfigParser(2.2)

# fix HiDpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)


def toggle_theme():
    """Switch themes"""
    if configParser.get("dark_mode"):
        yin_yang.switch_to_dark()
    else:
        yin_yang.switch_to_light()


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
            mode = configParser.get("mode")
            if mode == config.Modes.manual.value:
                print("looks like you did not specified a time")
                print("You can use the gui with yin-yang -gui")
                print("Or edit the config found in ~/.config/yin_yang/yin_yang.json")
                print("You need to set schedule to True and edit the time to toggles")
            else:
                print(f"Using mode {mode}")
        elif args.toggle:
            # toggle theme manually
            configParser.update("mode", config.Modes.manual.value)
            toggle_theme()


if __name__ == "__main__":
    main()
    if configParser.get("mode") != config.Modes.manual.value:
        configParser.update("running", False)
        print("START thread listener")
        yin_yang.start_daemon()
