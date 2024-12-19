import os
from contextlib import suppress

import loguru
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, Message

from bot.core.text_manager import ResourceType, resource_manager

logger = loguru.logger
bot = Bot(os.environ.get("BOT_TOKEN"))


def text(key: ResourceType) -> str | None:
    return resource_manager.get_text(key)


async def set_bot_commands() -> None:
    command_texts = resource_manager.commands
    commands = [BotCommand(command=cmd, description=desc) for cmd, desc in command_texts.items()]
    await bot.set_my_commands(commands)


async def send_msg_to_admin(text: str, message: Message) -> None:
    await bot.send_message(
        chat_id=os.getenv("CHAT_ID"),
        message_thread_id=os.getenv("THREAD_ID"),
        text=text,
    )
    with suppress(TelegramBadRequest):
        await message.delete()
