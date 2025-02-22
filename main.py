import asyncio
import logging
from bot import app, db

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting RihnoBot...")
    await app.start()
    await asyncio.Future()  # Run indefinitely
    await app.stop()
    await db.close()
    logger.info("RihnoBot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")