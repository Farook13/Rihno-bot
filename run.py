import sys
import subprocess

def run_bot():
    """Run the main bot script."""
    subprocess.run([sys.executable, "bot.py"])

def populate_database():
    """Populate the database with sample data."""
    subprocess.run([sys.executable, "populate_db.py"])

def print_help():
    """Display usage information."""
    print("""
Telegram AutoFilter Bot Runner

Usage:
  python run.py <command>

Commands:
  bot         Run the Telegram bot
  populate    Populate the MongoDB database with sample data
  help        Show this help message
    """)

if __name__ == "__main__":
    # Check if a command is provided
    if len(sys.argv) < 2:
        print("Error: No command provided.")
        print_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "bot":
        run_bot()
    elif command == "populate":
        populate_database()
    elif command == "help":
        print_help()
    else:
        print(f"Error: Unknown command '{command}'.")
        print_help()
        sys.exit(1)
