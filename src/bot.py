from aiogram import Bot, Dispatcher

from src.config import BOT_TOKEN
from src.handlers.start import router as start_router
from src.handlers.subjects import router as subjects_router
from src.handlers.tasks import router as tasks_router
from src.handlers.settings import router as settings_router
from src.handlers.statistics import router as statistics_router


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(subjects_router)
dp.include_router(tasks_router)
dp.include_router(settings_router)
dp.include_router(statistics_router)
