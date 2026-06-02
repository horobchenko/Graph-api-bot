import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.start import router
from config.logging import setup_logging
from config.settings import BOT_TOKEN


async def main() -> None:
    logger = setup_logging()
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not configured. Please add it to your .env file.")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
