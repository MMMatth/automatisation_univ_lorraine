#!/bin/bash

cd /home/matth/server/univ-lorraine/src/
source ../myenv/bin/activate
echo "Execution de discord_server.sh le $(date)"
echo $(python3 discord_bot.py)