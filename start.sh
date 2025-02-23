#!/bin/bash
set -e
echo "Starting the Telegram Movie Bot..."
if ! command -v python3 &> /dev/null; then
 echo "Python3 not installed."
 exit 1
fi
if [ -f "requirements.txt" ]; then
 pip3 install --no-cache-dir -r requirements.txt
fi
python3 bot.py