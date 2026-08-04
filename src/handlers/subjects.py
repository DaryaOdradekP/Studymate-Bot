from aiogram import Router, F
from aiogram.types import Message
from src.keyboards.subjects_menu import subjects_menu

router = Router()


@router.message(F.text == "Subjects")
async def subjects_handler(message: Message):
    await message.answer(
        text = "Subject menu",
        reply_markup=subjects_menu,
    )
