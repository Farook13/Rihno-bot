from pyrogram import Client, filters
from handlers import start, filter, admin

app = Client(
    "AutoFilterBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Register handlers
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await start.start_command(client, message)

@app.on_message(filters.text & ~filters.command(["start", "add", "delete"]))
async def filter_cmd(client, message):
    await filter.filter_handler(client, message)

# Admin commands
@app.on_message(filters.command("add"))
async def add_file_cmd(client, message):
    await admin.add_file(client, message)

@app.on_message(filters.command("delete"))
async def delete_file_cmd(client, message):
    await admin.delete_file(client, message)

if __name__ == "__main__":
    print("Bot starting...")
app = Bot()
app.run()
