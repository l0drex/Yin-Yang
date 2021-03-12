#!/bin/bash

pyuic5 -o ../yin_yang/ui/mainwindow.py ../designer/mainwindow.ui
rcc -g python ../resources.qrc > ../yin_yang/ui/resources_rc.py
