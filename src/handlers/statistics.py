from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "Statistics")
async def statistics_handler(message: Message):
    await message.answer("Statistics menu")
