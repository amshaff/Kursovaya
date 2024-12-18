from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть число отправленных сообщений", callback_data='attempts'), InlineKeyboardButton(text="Помощь", callback_data='help')],
    [InlineKeyboardButton(text="Перефразировать текст", callback_data='rephrase')]
])

choice_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Да", callback_data="rephrase"),
    InlineKeyboardButton(text="Нет", callback_data="start")
]])

help_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="start")]])