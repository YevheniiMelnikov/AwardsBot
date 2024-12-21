import os
from contextlib import suppress

import loguru
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommand, Message, CallbackQuery

from bot.core.api_service import api_service
from bot.core.text_manager import ResourceType, resource_manager

logger = loguru.logger
bot = Bot(os.environ.get("BOT_TOKEN"))


def text(key: ResourceType) -> str | None:
    return resource_manager.get_text(key)


async def set_bot_commands() -> None:
    command_texts = resource_manager.commands
    assert command_texts
    if commands := [BotCommand(command=cmd, description=desc) for cmd, desc in command_texts.items()]:
        await bot.set_my_commands(commands)
    else:
        logger.warning("No commands to set")


async def send_msg_to_admin(msg_text: str, message: Message) -> None:
    await bot.send_message(
        chat_id=os.getenv("CHAT_ID"),
        message_thread_id=os.getenv("THREAD_ID"),
        text=msg_text,
    )
    with suppress(TelegramBadRequest):
        await message.delete()


async def process_vote(call: CallbackQuery, data: dict[str, str]) -> bool:
    nominations = await api_service.get_all_nominations()
    nomination = next((n for n in nominations if n.name == data.get("nomination")), None)
    candidates = await api_service.get_all_candidates()
    candidate = next((c for c in candidates if c.username == call.data), None)
    candidate_nomination = next((n for n in candidate.nominations if n.nomination == nomination.id), None)

    if await api_service.increment_vote(
        nomination_id=candidate_nomination.id, new_votes_count=candidate_nomination.votes_count + 1
    ):
        await api_service.create_vote(
            user_tg_id=call.from_user.id,
            nomination_id=nomination.id,
            candidate_id=candidate.id,
        )
        return True

    return False
