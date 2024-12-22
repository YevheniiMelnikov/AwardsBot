from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.functions import accept_candidate, reject_candidate

admin_router = Router()


@admin_router.callback_query(F.data.startswith("accept"))
@admin_router.callback_query(F.data.startswith("reject"))
async def handle_candidate(call: CallbackQuery) -> None:
    action, candidate_id, nomination = call.data.split("-")
    if action == "accept":
        await call.answer("✅")
        await accept_candidate(candidate_id, nomination)
    else:
        await call.answer("❌")
        await reject_candidate(candidate_id)

    await call.message.delete()
