from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    kb.row(InlineKeyboardButton(text=text(ButtonText.channel_of_the_year), callback_data="channel_of_the_year"))
    kb.row(
        InlineKeyboardButton(text=text(ButtonText.admin_of_the_year), callback_data="admin_of_the_year"),
        InlineKeyboardButton(text=text(ButtonText.theme_of_the_year), callback_data="theme_of_the_year"),
    )
    kb.row(
        InlineKeyboardButton(
            text=text(ButtonText.content_creator_of_the_year), callback_data="content_creator_of_the_year"
        ),
        InlineKeyboardButton(text=text(ButtonText.manager_of_the_year), callback_data="manager_of_the_year"),
    )
    kb.row(
        InlineKeyboardButton(text=text(ButtonText.blog_of_the_year), callback_data="blog_of_the_year"),
        InlineKeyboardButton(text=text(ButtonText.welcome_bot_of_the_year), callback_data="welcome_bot_of_the_year"),
    )
    kb.row(
        InlineKeyboardButton(text=text(ButtonText.posting_bot_of_the_year), callback_data="posting_bot_of_the_year"),
        InlineKeyboardButton(text=text(ButtonText.buyer_of_the_year), callback_data="buyer_of_the_year"),
    )
    kb.row(
        InlineKeyboardButton(text=text(ButtonText.admin_chat_of_the_year), callback_data="admin_chat_of_the_year"),
        InlineKeyboardButton(text=text(ButtonText.info_gypsy_of_the_year), callback_data="info_gypsy_of_the_year"),
    )
    kb.row(
        InlineKeyboardButton(text=text(ButtonText.scam_of_the_year), callback_data="scam_of_the_year"),
        InlineKeyboardButton(text=text(ButtonText.clown_of_the_year), callback_data="clown_of_the_year"),
    )
    return kb.as_markup()
