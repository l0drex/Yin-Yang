#!/bin/bash

# requires sudo
if test ${EUID} -ne 0; then
    kdialog --password "Changing the times in the systemd timer requires sudo rights" | exec sudo -S "$0" "$@"
    exit 0
fi

echo number of  arguments: $#
echo "$1"
echo "$2"

cat > "/usr/lib/systemd/system/yin-yang.timer" <<EOF
[Unit]
Description=Switch the theme between light and dark automatically

[Timer]
OnActiveSec=2s
# these values will be changed by the config
OnCalendar=*-*-* $1
OnCalendar=*-*-* $2

[Install]
# enable on boot
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl start yin-yang.timer
