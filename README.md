# Telegram AutoFilter Bot

A Telegram bot that searches files from a MongoDB database with force subscribe, auto-delete, and fast response (within 3 seconds).

## Features
- **Autofilter**: Search files stored in MongoDB by sending a query.
- **Force Subscribe**: Users must join a specified channel to use the bot.
- **Auto-Delete**: Messages are deleted after a configurable time (default: 60 seconds).
- **Fast Response**: Optimized to reply within 3 seconds.
- **Utilities**: Example command (`/addfile`) for the owner to add files.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Telegram-AutoFilter-Bot.git
   cd Telegram-AutoFilter-Bot
