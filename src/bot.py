from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN
from src.handlers.start import router

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

dp.include_router(router)
