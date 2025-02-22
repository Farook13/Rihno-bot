import asyncio
import logging
import logging.config  # Add this import
from aiohttp import web
from bot import app, db

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK", status=200)

async def run_http_server():
    app_web = web.Application()
    app_web.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    logger.info("Health check server running on port 8000")
    return runner

async def main():
    logger.info("Starting RihnoBot...")
    http_runner = await run_http_server()
    try:
        await app.start()
        await asyncio.Future()
    finally:
        await app.stop()
        await db.close()
        await http_runner.cleanup()
        logger.info("RihnoBot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")