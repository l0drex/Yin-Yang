#!/bin/bash

rcc -g python ./resources.qrc > ./yin_yang/ui/resources_rc.py
pyuic5 -o ./yin_yang/ui/main_window.py ./designer/main_window.ui
pylupdate5 yin-yang.pro
