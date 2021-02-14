#!/bin/bash

# this script will uninstall Yin-Yang and will also delete its config files

set -euo pipefail

home=${HOME}

# check, if sudo
if test ${EUID} -ne 0; then
    echo enter password in order to install Yin-Yang correctly
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo "Removing config and .desktop file"
rm -rf "${home}"/.local/share/applications/Yin-Yang.desktop
rm -rf "${home}"/.config/yin_yang

echo "Removing program and terminal execution"
rm -rf /opt/yin-yang /usr/bin/yin-yang.sh
systemctl disable yin-yang.timer
rm /usr/lib/systemd/system/yin-yang.timer
rm /usr/lib/systemd/system/yin-yang.service

echo Yin-Yang uninstalled succesfully
echo have a nice day ...
