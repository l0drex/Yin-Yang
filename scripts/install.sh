#!/bin/bash

set -euo pipefail

if test ${EUID} -ne 0; then
    echo "Enter password in order to install Yin-Yang correctly."
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo
echo "Removing old Yin-Yang files if they exist."
./scripts/uninstall.sh "${HOME}"

echo
echo "Installing dependencies..."
pip3 install qtpy
pip3 install pyqt5
pip3 install suntime

echo
echo "Creating directories..."
# check if /opt/ directory exists else create
if [ ! -d /opt/ ]; then
    mkdir -p /opt/
fi
if [ ! -d /opt/yin-yang/ ]; then
    mkdir -p /opt/yin-yang/
fi
if [ ! -d ${HOME}/.local/share/applications/ ]; then
    mkdir -p ${HOME}/.local/share/applications/
fi

echo
echo "Installing Yin-Yang..."
# copy files
cp -r ./* /opt/yin-yang/
# copy terminal executive
cp ./scripts/yin-yang /usr/bin/
chmod +x /usr/bin/yin-yang

echo
echo "Creating .desktop file for native environment execution..."
cp ./resources/Yin-Yang.desktop ${HOME}/.local/share/applications/Yin-Yang.desktop

cat << "EOF"
 __     ___          __     __
 \ \   / (_)         \ \   / /
  \ \_/ / _ _ __ _____\ \_/ /_ _ _ __   __ _
   \   / | | '_ \______\   / _` | '_ \ / _` |
    | |  | | | | |      | | (_| | | | | (_| |
    |_|  |_|_| |_|      |_|\__,_|_| |_|\__, |
                                        __/ |
                                       |___/
EOF
echo
echo "Welome to Yin-Yang! Activate auto dark mode for various applications by starting the application."
echo

cat << "EOF"
       _..oo8"""Y8b.._
     .88888888o.    "Yb.
   .d888P""Y8888b      "b.
  o88888    88888)       "b
 d888888b..d8888P         'b
 88888888888888"           8
(88DWB8888888P             8)
 8888888888P               8
 Y88888888P     ee        .P
  Y888888(     8888      oP
   "Y88888b     ""     oP"
     "Y8888o._     _.oP"
       `""Y888boodP""'

EOF

echo "Checkout https://github.com/daehruoydeef/Yin-Yang if your need help."
echo "Yin-Yang is now installed."
