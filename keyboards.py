from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def button(url: str, availability_0_0: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='◀', callback_data='back'),
        types.InlineKeyboardButton(text=availability_0_0, callback_data='AVAILABILITY'),
        types.InlineKeyboardButton(text='▶', callback_data='NEXT')
    ).row(
        types.InlineKeyboardButton(text='Reference', url=url)
    )
    return builder.as_markup()