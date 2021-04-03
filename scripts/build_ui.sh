#!/bin/bash

pyrcc5 ./resources.qrc -o ./resources_rc.py
pyuic5 -o ./yin_yang/ui/main_window.py ./designer/main_window.ui
pylupdate5 yin-yang.pro
