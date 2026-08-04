from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "Tasks")
async def tasks_handler(message: Message):
    await message.answer("Tasks menu")
