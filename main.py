from aiogram import Dispatcher, Bot
from program_logic.handlers.handlers import router, init_data
from dotenv import load_dotenv
from os import getenv


load_dotenv()

TOKEN = getenv("TOKEN")
print (TOKEN)
AUTH_TOKEN = getenv("AUTH_TOKEN")
db_path = "program_logic/database/users.db"
sql_path = "program_logic/database/db.sql"

init_data(sql_path, db_path, AUTH_TOKEN)

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)

dp.run_polling(bot)
