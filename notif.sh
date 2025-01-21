#!/bin/bash

cd /home/matth/server/univ-lorraine/src/
source ../myenv/bin/activate
# print date
echo "Execution de notif.sh le $(date)"
echo $(python3 send_notification.py)