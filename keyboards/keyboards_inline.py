from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from data import TEXT_BOT

text_keyboards = TEXT_BOT.KeyboardsText

inline_buttons_settings = [[InlineKeyboardButton(text=text_keyboards['all'], callback_data='all')],
                           [InlineKeyboardButton(text=text_keyboards['chat'], callback_data='chat')],
                           [InlineKeyboardButton(text=text_keyboards['file'], callback_data='file')]]

inline_buttons_found_values = [[InlineKeyboardButton(text=text_keyboards['insert_values'], callback_data='insert')],
                               [InlineKeyboardButton(text=text_keyboards['not_insert_values'],
                                                     callback_data='not_insert')]]

kb_inline_settings_user = InlineKeyboardMarkup(inline_keyboard=inline_buttons_settings)
kb_inline_found_values = InlineKeyboardMarkup(inline_keyboard=inline_buttons_found_values)
