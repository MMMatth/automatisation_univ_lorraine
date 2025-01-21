#!/bin/bash

PIDFILE=/home/matth/server/pid/discord_bot.pid

# Function to start the bot
start_bot() {
    cd /home/matth/server/univ-lorraine/src/
    source ../myenv/bin/activate
    echo "Execution de discord_server.sh le $(date)"
    python3 discord_bot/discord_bot.py &
    echo $! > $PIDFILE
    echo "Bot started with PID $(cat $PIDFILE)"
}

# Check if PID file exists
if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    if ps -p $PID > /dev/null; then
        echo "Bot is running with PID $PID, stopping it..."
        kill $PID
        rm $PIDFILE
        echo "Bot stopped."
    else
        echo "PID file found but no process with PID $PID, starting new bot..."
        rm $PIDFILE
    fi
fi

# Start the bot
start_bot