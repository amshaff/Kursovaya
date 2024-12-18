from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from program_logic.database.db import UserDatabase, check_db
from program_logic.send_data.lexicon import *
from program_logic.send_data.keyboards import *
from program_logic.gigachat_api.gigachat_api import send_to_rephrase
from os.path import join, abspath, dirname


router = Router()


class BotState(StatesGroup):
    default = State()
    rephrase_text_await = State()
    

def init_data(sql_path_val, db_path_val, auth):
    global sql_path, db_path, AUTH_TOKEN
    sql_path = sql_path_val
    db_path = db_path_val
    AUTH_TOKEN = auth


@router.message(Command("start"))
async def send_welcome(message: Message, state: FSMContext):
    check_db(message.from_user, db_path, sql_path)

    await state.set_state(BotState.default)
    
    await message.answer(welcome_message, reply_markup=start_kb)
     
@router.callback_query(lambda a: a.data == "start")
async def send_welcome(callback: CallbackQuery, state: FSMContext):

    await callback.answer("")
    await state.set_state(BotState.default)
    await callback.message.answer(welcome_message, reply_markup=start_kb)

@router.message(Command("help"))
async def help(message: Message):
    check_db(message.from_user, db_path, sql_path)
    await message.answer(help_message, reply_markup=help_button)
    
@router.callback_query(lambda a: a.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(help_message, reply_markup=help_button)
    
@router.callback_query(lambda a: a.data == "attempts")
async def attempts_callback(callback: CallbackQuery):
    await callback.answer("")
    with UserDatabase(db_path, sql_path) as db:
        await callback.message.answer(count_message.format(num=db.get_att(callback.from_user)), reply_markup=help_button)
    
@router.callback_query(lambda a: a.data == "rephrase")
async def rephrase_callback(callback: CallbackQuery, state: FSMContext):
    check_db(callback.from_user, db_path, sql_path)
    await callback.answer(request_message)
    await state.set_state(BotState.rephrase_text_await)
    await callback.message.answer(request_message)
    
@router.message(BotState.rephrase_text_await)
async def rephrase_message(message: Message, state: FSMContext):
    await message.answer((await send_to_rephrase(str(message.text), auth_token=AUTH_TOKEN))["choices"][0]["message"]["content"])

    with UserDatabase(db_path, sql_path) as db:
        db.inc_att(message.from_user)
        
    await message.answer(ask_message, reply_markup=choice_kb)

@router.message()
async def answer_default(message: Message):
    await help(message)