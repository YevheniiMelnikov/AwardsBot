import asyncio
import os

import loguru
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from bot.handlers.admin_handler import admin_router
from bot.handlers.command_handler import cmd_router
from bot.functions import set_bot_commands
from bot.handlers.main_handler import main_router

load_dotenv()
logger = loguru.logger


async def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN environment variable not found.")
        return

    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    assert bot
    redis_url = os.getenv("REDIS_HOST")
    await set_bot_commands()
    dp = Dispatcher(storage=RedisStorage.from_url(f"{redis_url}/0"))
    dp.include_routers(cmd_router, admin_router, main_router)

    logger.info("Starting bot ...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Failed to start the bot due to an exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
