from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "Settings")
async def settings_handler(message: Message):
    await message.answer("Settings menu")
