#!/bin/bash

# This script will uninstall Yin-Yang and will also delete its config files

set -euo pipefail

# check, if sudo
if test ${EUID} -ne 0; then
    echo "Enter password in order to install Yin-Yang correctly"
    echo
    exec sudo su -c "${0} ${HOME}"
    exit 0
fi

echo "Removing config and .desktop file..."
rm -rf ${HOME}/.local/share/applications/Yin-Yang.desktop
rm -rf ${HOME}/.config/yin_yang

echo "Removing program and terminal execution"
rm -rf /opt/yin-yang /usr/bin/yin-yang.sh

echo
echo Yin-Yang uninstalled succesfully.
