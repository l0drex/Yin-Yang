#!/bin/bash

# requires sudo
if test ${EUID} -ne 0; then
    echo Changing the times in the systemd timer requires sudo rights
    exec sudo -A su -c "${0} ${HOME}"
    exit 0
fi

cat > "/usr/lib/systemd/system/yin-yang.timer" <<EOF
[Unit]
Description=Switch the theme between light and dark automatically

[Timer]
OnBootSec=5
# these values will be changed by the config
OnCalendar=*-*-* 07:00:00
OnCalendar=*-*-* 20:00:00

[Install]
# enable on boot
WantedBy=timers.target
EOF
