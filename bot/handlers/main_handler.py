from contextlib import suppress

import loguru
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.api_service import api_service
from bot.functions import text, process_vote
import bot.keyboards as kb
from bot.states import States
from bot.resources.texts import MessageText
from bot.utils import get_photo, get_nomination_verbose

main_router = Router()
logger = loguru.logger


@main_router.callback_query(States.select_nomination)
async def select_nomination(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.answer_photo(
        get_photo("nominations"), caption=text(MessageText.select_nomination), reply_markup=kb.select_nomination()
    )
    await call.message.delete()
    await state.set_state(States.vote_menu)


@main_router.callback_query(States.vote_menu)
async def vote_menu(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(nomination=call.data)
    candidates = await api_service.get_candidates(call.data)
    await call.message.answer_photo(
        get_photo(call.data),
        caption=text(MessageText.choose_candidate),
        reply_markup=kb.choose_candidate(candidates),
    )
    await state.set_state(States.get_vote)


@main_router.callback_query(States.get_vote)
async def get_vote(call: CallbackQuery, state: FSMContext) -> None:
    match call.data:
        case "back":
            await state.set_state(States.select_nomination)
            await state.clear()
            await call.message.answer_photo(
                get_photo("nominations"),
                caption=text(MessageText.select_nomination),
                reply_markup=kb.select_nomination(),
            )

        case "new_candidate":
            data = await state.get_data()
            nom_verbose = get_nomination_verbose(data.get("nomination"))
            await state.update_data(nom_verbose=nom_verbose)
            await call.message.answer(
                text(MessageText.new_candidate).format(nomination=nom_verbose), reply_markup=kb.back()
            )
            await state.set_state(States.new_candidate)

        case _:
            await call.answer(text(MessageText.vote_accepted), show_alert=True)
            await process_vote(call, state)
            await state.set_state(States.select_nomination)
            await state.clear()
            await call.message.answer_photo(
                get_photo("nominations"),
                caption=text(MessageText.select_nomination),
                reply_markup=kb.select_nomination(),
            )

    with suppress(TelegramBadRequest):
        await call.message.delete()


@main_router.callback_query(States.new_candidate)
@main_router.message(States.new_candidate)
async def new_candidate(event: CallbackQuery | Message, state: FSMContext) -> None:
    if isinstance(event, CallbackQuery):
        data = await state.get_data()
        nom = data.get("nomination")
        candidates = await api_service.get_candidates(nom)
        await event.message.answer_photo(
            get_photo(nom),
            caption=text(MessageText.choose_candidate),
            reply_markup=kb.choose_candidate(candidates),
        )
        await state.set_state(States.get_vote)
        await event.message.delete()
    else:
        await event.answer(text(MessageText.candidate_description), reply_markup=kb.back())
        await state.update_data(candidate=event.text)
        await state.set_state(States.candidate_description)
        await event.delete()


@main_router.callback_query(States.candidate_description)
@main_router.message(States.candidate_description)
async def candidate_description(event: CallbackQuery | Message, state: FSMContext) -> None:
    if isinstance(event, CallbackQuery):
        data = await state.get_data()
        nom_verbose = data.get("nom_verbose")
        await event.message.answer(
            text(MessageText.new_candidate).format(nomination=nom_verbose), reply_markup=kb.back()
        )
        await state.set_state(States.new_candidate)
    else:
        await event.answer(text(MessageText.candidate_request), reply_markup=kb.main_menu())
        await state.update_data(candidate_description=event.text)
        await state.set_state(States.select_nomination)
        # TODO: SEND REQUEST TO ADMIN
