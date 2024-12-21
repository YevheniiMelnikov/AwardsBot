import loguru
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import bot.keyboards as kb
from bot.core.api_service import api_service
from bot.states import States
from bot.functions import text
from bot.resources.texts import MessageText
from bot.utils import get_photo

cmd_router = Router()
logger = loguru.logger


@cmd_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started the bot")
    await state.clear()
    await message.answer_photo(get_photo("welcome"), caption=text(MessageText.greetings), reply_markup=kb.launch())
    if not await api_service.get_user_by_tg(message.from_user.id):
        await api_service.create_user(message)
    await state.set_state(States.select_nomination)
