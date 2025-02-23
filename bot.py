from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import BOT_TOKEN, LOGGER, SUPPORT_CHAT
from database import Database
from utils import get_file_size

db = Database()

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Welcome! Forward movie files to index them.\nSupport: {SUPPORT_CHAT}")

def handle_file(update: Update, context: CallbackContext):
    message = update.message
    if not (message.document or message.video):
        update.message.reply_text("Please forward a document or video file.")
        return

    file = message.document or message.video
    file_data = {
        "file_id": file.file_id,
        "file_name": file.file_name if hasattr(file, "file_name") else "Unnamed",
        "caption": message.caption or "",
        "size": get_file_size(file),
        "chat_id": message.chat_id,
        "message_id": message.message_id
    }
    if db.insert_file(file_data):
        update.message.reply_text(f"Indexed: {file_data['file_name']}")
    else:
        update.message.reply_text("File already indexed.")

def search(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        update.message.reply_text("Use: /search <query>")
        return

    results = db.search_files(query)
    if not results:
        update.message.reply_text("No results found.")
        return

    response = "Found:\n"
    for i, r in enumerate(results, 1):
        response += f"{i}. {r['file_name']} ({r['size']})\n"
    update.message.reply_text(response)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(MessageHandler(Filters.forwarded & (Filters.document | Filters.video), handle_file))

    LOGGER.info("Bot started.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​