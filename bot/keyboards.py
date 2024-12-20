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
