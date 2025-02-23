#!/bin/bash
set -e
echo "Starting the Telegram Movie Bot..."
ls -la  # List files to confirm presence
python3 --version  # Confirm Python version
pip3 list  # Confirm installed packages
if [ -f "bot.py" ]; then
    python3 bot.py
else
    echo "bot.py not found!"
    exit 1
fi
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing it now..."
    sudo apt-get update && sudo apt-get install -y python3-pip
fi

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip3 install --no-cache-dir -r requirements.txt
else
    echo "requirements.txt not found! Please ensure it exists in the project directory."
    exit 1
fi

# Check if bot.py exists
if [ -f "bot.py" ]; then
    echo "Starting the bot..."
    python3 bot.py
else
    echo "bot.py not found! Please ensure the main bot script exists."
    exit 1
fi

# Keep the script running (optional, for environments like Docker)
# Uncomment the line below if you want the script to keep the container alive
# tail -f /dev/null