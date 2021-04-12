#!/bin/bash

# resource file
pyrcc5 ../resources.qrc -o ../resources_rc.py
# ui file from qt designer
pyuic5 -o ../yin_yang/ui/main_window.py ../designer/main_window.ui
# translation files
pylupdate5 ../yin-yang.pro
