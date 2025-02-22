import asyncio
import random
from pyrogram import Client, filters, idle
from aiohttp import web
from config import Config
from handlers import start, filter, admin

# Telegram bot setup
app = Client("RihnoBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
start.register(app)
filter.register(app)
admin.register(app)

# Dummy HTTP server for health check
async def health_check(request):
    return web.Response(text="OK", status=200)

async def run_http_server():
    try:
        app_web = web.Application()
        app_web.add_routes([web.get('/', health_check)])
        runner = web.AppRunner(app_web)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8000)
        await site.start()
        print("Health check server running on port 8000")
        return runner  # Return runner to keep it alive
    except Exception as e:
        print(f"Failed to start HTTP server: {e}")
        raise

async def main():
    print("Starting Rihno Bot...")
    # Start HTTP server first and ensure it’s running
    http_runner = await run_http_server()
    try:
        await app.start()
        await idle()
    except Exception as e:
        print(f"Failed to start bot: {e}")
    finally:
        await app.stop()
        await http_runner.cleanup()
        print("Rihno Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())
