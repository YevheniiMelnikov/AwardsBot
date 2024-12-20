import loguru
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.api_service import api_service
from bot.functions import send_msg_to_admin, text
import bot.keyboards as kb
from bot.states import States
from bot.resources.texts import MessageText
from bot.utils import get_photo

main_router = Router()
logger = loguru.logger


@main_router.callback_query(States.select_nomination)
async def select_nomination(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer_photo(
        get_photo("nominations"), caption=text(MessageText.select_category), reply_markup=kb.select_nomination()
    )
    await call.message.delete()
    await state.set_state(States.vote_menu)


@main_router.callback_query(States.vote_menu)
async def vote_menu(call: CallbackQuery, state: FSMContext) -> None:
    candidates = await api_service.get_candidates(call.data)
    await call.message.answer_photo(get_photo("candidates"))


@main_router.message(States.feedback)
async def feedback(message: Message, state: FSMContext) -> None:
    await message.answer(text(MessageText.feedback_sent), reply_markup=kb.ok())
    username = message.from_user.username if message.from_user.username else message.from_user.id
    await send_msg_to_admin(text(MessageText.incoming_feedback).format(user=username, message=message.text), message)
    logger.info(f"User {username} sent feedback")
    await state.set_state(States.select_nomination)
