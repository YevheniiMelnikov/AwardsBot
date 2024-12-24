from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as Btn
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.functions import text
from bot.resources.texts import ButtonText


def launch() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text(ButtonText.launch), callback_data="launch")
    return kb.as_markup(one_time_keyboard=True)


def ok() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text(ButtonText.ok), callback_data="ok")
    return kb.as_markup(one_time_keyboard=True)


def back() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text(ButtonText.back), callback_data="back")
    return kb.as_markup(one_time_keyboard=True)


def select_nomination() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(Btn(text=text(ButtonText.channel_nom), callback_data="channel_nom"))
    kb.row(
        Btn(text=text(ButtonText.admin_nom), callback_data="admin_nom"),
        Btn(text=text(ButtonText.theme_nom), callback_data="theme_nom"),
    )
    kb.row(
        Btn(text=text(ButtonText.content_creator_nom), callback_data="content_creator_nom"),
        Btn(text=text(ButtonText.manager_nom), callback_data="manager_nom"),
    )
    kb.row(
        Btn(text=text(ButtonText.blog_nom), callback_data="blog_nom"),
        Btn(text=text(ButtonText.welcome_bot_nom), callback_data="welcome_bot_nom"),
    )
    kb.row(
        Btn(text=text(ButtonText.posting_bot_nom), callback_data="posting_bot_nom"),
        Btn(text=text(ButtonText.buyer_nom), callback_data="buyer_nom"),
    )
    kb.row(
        Btn(text=text(ButtonText.admin_chat_nom), callback_data="admin_chat_nom"),
        Btn(text=text(ButtonText.info_gypsy_nom), callback_data="info_gypsy_nom"),
    )
    kb.row(
        Btn(text=text(ButtonText.scam_nom), callback_data="scam_nom"),
        Btn(text=text(ButtonText.clown_nom), callback_data="clown_nom"),
    )
    return kb.as_markup()


def choose_candidate(candidates: dict[str, int]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if candidates:
        sorted_candidates = sorted(candidates.items(), key=lambda item: item[1], reverse=True)
        for username, votes in sorted_candidates:
            kb.button(text=f"[{votes} 👑] {username}", callback_data=username)
            kb.adjust(1)

    kb.button(text=text(ButtonText.new_candidate), callback_data="new_candidate")
    kb.adjust(1)
    kb.button(text=text(ButtonText.back), callback_data="back")
    kb.adjust(1)
    return kb.as_markup()



def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text(ButtonText.main_menu), callback_data="main_menu")
    return kb.as_markup(one_time_keyboard=True)


def handle_candidate_request(data: dict[str, str]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    username = data.get("username")
    nom = data.get("nomination")
    kb.button(text=text(ButtonText.accept), callback_data=f"accept-{username}-{nom}")
    kb.button(text=text(ButtonText.reject), callback_data=f"reject-{username}-{nom}")
    return kb.as_markup(one_time_keyboard=True)
