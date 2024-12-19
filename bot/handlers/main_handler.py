import loguru
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.functions import send_msg_to_admin, text
import bot.keyboards as kb
from bot.states import States
from bot.resources.texts import MessageText

main_router = Router()
logger = loguru.logger


@main_router.callback_query(States.select_category)
async def select_category(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text(MessageText.select_category), reply_markup=kb.select_nomination())
    await call.message.delete()


@main_router.message(States.feedback)
async def feedback(message: Message, state: FSMContext) -> None:
    await message.answer(text(MessageText.feedback_sent), reply_markup=kb.ok())
    username = message.from_user.username if message.from_user.username else message.from_user.id
    await send_msg_to_admin(text(MessageText.incoming_feedback).format(user=username, message=message.text), message)
    logger.info(f"User {username} sent feedback")
    await state.set_state(States.select_category)
