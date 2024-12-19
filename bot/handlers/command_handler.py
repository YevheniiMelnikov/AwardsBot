import loguru
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import bot.keyboards as kb
from bot.states import States
from bot.core import api_service
from bot.functions import text
from bot.resources.texts import MessageText

cmd_router = Router()
logger = loguru.logger


@cmd_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started the bot")
    await state.clear()
    await message.answer(text(MessageText.greetings), reply_markup=kb.launch())
    if not await api_service.get_user(message.from_user.id):
        await api_service.create_user(message)
    await state.set_state(States.select_category)


@cmd_router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(text(MessageText.help))
    await state.set_state(States.feedback)
