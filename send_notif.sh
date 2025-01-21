#!/bin/bash

PIDFILE=/home/matth/server/pid/send_notification.pid

# Function to start the notification script
start_notification() {
    cd /home/matth/server/univ-lorraine/src/
    source ../myenv/bin/activate
    echo "Execution de notif.sh le $(date)"
    python3 discord_bot/send_notification.py &
    echo $! > $PIDFILE
    echo "Notification script started with PID $(cat $PIDFILE)"
}

# Check if PID file exists
if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    if ps -p $PID > /dev/null; then
        echo "Notification script is running with PID $PID, stopping it..."
        kill $PID
        rm $PIDFILE
        echo "Notification script stopped."
    else
        echo "PID file found but no process with PID $PID, starting new notification script..."
        rm $PIDFILE
    fi
fi

# Start the notification script
start_notification