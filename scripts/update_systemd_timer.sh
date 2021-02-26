#!/bin/bash

# requires sudo
if test ${EUID} -ne 0; then
    kdialog --password "Changing the times in the systemd timer requires sudo rights" | exec sudo -S "$0" "$@"
    exit 0
fi

# disable timer, if it isn't needed
if [ "$1" == "0" ]; then
  echo "Timer is not needed, disabling it now"
  systemctl stop yin-yang.timer
  systemctl disable yin-yang.timer
  exit 0
fi

cat > "/usr/lib/systemd/system/yin-yang.timer" <<EOF
[Unit]
Description=Switch the theme between light and dark automatically

[Timer]
OnActiveSec=2s
OnBootSec=5s
OnCalendar=*-*-* $2
OnCalendar=*-*-* $3

[Install]
# enable on boot
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable yin-yang.timer
systemctl start yin-yang.timer
