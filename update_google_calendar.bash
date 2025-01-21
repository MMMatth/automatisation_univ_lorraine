#!/bin/bash

PIDFILE=/home/matth/server/pid/update_google_calendar.pid

# Function to start the update script
start_update() {
    cd /home/matth/server/univ-lorraine/src/
    source ../myenv/bin/activate
    echo "Execution de update_google_calendar.bash le $(date)"
    python3 main.py &
    echo $! > $PIDFILE
    echo "Update script started with PID $(cat $PIDFILE)"
}

# Check if PID file exists
if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    if ps -p $PID > /dev/null; then
        echo "Update script is running with PID $PID, stopping it..."
        kill $PID
        rm $PIDFILE
        echo "Update script stopped."
    else
        echo "PID file found but no process with PID $PID, starting new update script..."
        rm $PIDFILE
    fi
fi

# Start the update script
start_update