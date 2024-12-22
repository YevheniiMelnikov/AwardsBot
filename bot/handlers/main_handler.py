import os
from contextlib import suppress

import httpx
import loguru
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.api_service import api_service
from bot.functions import text, process_vote
import bot.keyboards as kb
from bot.states import States
from bot.resources.texts import MessageText
from bot.utils import get_photo, get_nomination_verbose, map_candidates_to_votes

main_router = Router()
logger = loguru.logger


@main_router.callback_query(States.main_menu)
async def select_nomination(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.answer()
    await call.message.answer_photo(
        get_photo("nominations"), caption=text(MessageText.select_nomination), reply_markup=kb.select_nomination()
    )
    await state.set_state(States.vote_menu)
    await call.message.delete()


@main_router.callback_query(States.vote_menu)
async def vote_menu(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(nomination=call.data)
    user = await api_service.get_user_by_tg(call.from_user.id)
    assert user
    if await api_service.has_user_voted(user.tg_id, call.data):
        await call.answer(text(MessageText.already_voted), show_alert=True)
        return

    await call.answer()
    all_candidates = await api_service.get_all_candidates()
    candidate_nominations = await api_service.get_candidate_nominations(call.data)
    candidates_data = map_candidates_to_votes(all_candidates, candidate_nominations)
    await call.message.answer_photo(
        get_photo(call.data),
        caption=text(MessageText.choose_candidate),
        reply_markup=kb.choose_candidate(candidates_data),
    )
    await state.set_state(States.get_vote)
    await call.message.delete()


@main_router.callback_query(States.get_vote)
async def get_vote(call: CallbackQuery, state: FSMContext) -> None:
    match call.data:
        case "back":
            await call.answer()
            await state.clear()
            await state.set_state(States.vote_menu)
            await call.message.answer_photo(
                get_photo("nominations"),
                caption=text(MessageText.select_nomination),
                reply_markup=kb.select_nomination(),
            )

        case "new_candidate":
            await call.answer()
            data = await state.get_data()
            nom_verbose = get_nomination_verbose(data.get("nomination"))
            await state.update_data(nom_verbose=nom_verbose)
            enter_username = await call.message.answer(
                text(MessageText.new_candidate).format(nomination=nom_verbose), reply_markup=kb.back()
            )
            await state.update_data(del_msg_id=enter_username.message_id)
            await state.set_state(States.new_candidate)

        case _:
            await call.answer(text(MessageText.vote_accepted), show_alert=True)
            data = await state.get_data()
            if await process_vote(call, data):
                logger.info(f"User {call.from_user.id} voted for {call.data}")
            await state.clear()
            await state.set_state(States.vote_menu)
            await call.message.answer_photo(
                get_photo("nominations"),
                caption=text(MessageText.select_nomination),
                reply_markup=kb.select_nomination(),
            )

    with suppress(TelegramBadRequest):
        await call.message.delete()


@main_router.callback_query(States.new_candidate)
@main_router.message(States.new_candidate)
async def new_candidate(event: CallbackQuery | Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    del_msg_id = data.get("del_msg_id")
    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id=event.from_user.id, message_id=del_msg_id)

    if isinstance(event, CallbackQuery):
        await event.answer()
        nom = data.get("nomination")
        all_candidates = await api_service.get_all_candidates()
        candidate_nominations = await api_service.get_candidate_nominations(nom)
        candidates_data = map_candidates_to_votes(all_candidates, candidate_nominations)
        await event.message.answer_photo(
            get_photo(nom),
            caption=text(MessageText.choose_candidate),
            reply_markup=kb.choose_candidate(candidates_data),
        )
        await state.set_state(States.get_vote)
        await event.message.delete()
    else:
        if candidate_id := await api_service.create_candidate(event.text):
            description_msg = await event.answer(text(MessageText.candidate_description), reply_markup=kb.back())
            await state.update_data(
                username=event.text, candidate_id=candidate_id, del_msg_id=description_msg.message_id
            )
            await state.set_state(States.candidate_description)
            await event.delete()
            return

        await event.answer(text(MessageText.candidate_exists))


@main_router.callback_query(States.candidate_description)
@main_router.message(States.candidate_description)
async def candidate_description(event: CallbackQuery | Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()

    del_message_id = data.get("del_msg_id")
    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id=event.from_user.id, message_id=del_message_id)

    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            text(MessageText.new_candidate).format(nomination=data.get("nom_verbose")), reply_markup=kb.back()
        )
        await state.set_state(States.new_candidate)
        await event.message.delete()
    else:
        await event.answer(text(MessageText.candidate_request), reply_markup=kb.main_menu())
        candidate_data = {
            "username": data.get("username"),
            "candidate_id": data.get("candidate_id"),
            "nomination": data.get("nomination"),
            "nom_verbose": data.get("nom_verbose"),
            "description": event.text,
        }
        async with httpx.AsyncClient():
            await bot.send_message(
                chat_id=os.getenv("CHAT_ID"),
                message_thread_id=os.getenv("THREAD_ID"),
                text=text(MessageText.incoming_request).format(**candidate_data),
                reply_markup=kb.handle_candidate_request(candidate_data),
            )

        await state.clear()
        await state.set_state(States.request_sent)
        await event.delete()


@main_router.callback_query(States.request_sent)
async def request_sent(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.answer_photo(
        get_photo("nominations"),
        caption=text(MessageText.select_nomination),
        reply_markup=kb.select_nomination(),
    )
    await state.set_state(States.vote_menu)
