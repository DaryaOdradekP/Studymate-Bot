from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "Subjects")
async def subjects_handler(message: Message):
    await message.answer("Subjects menu")
