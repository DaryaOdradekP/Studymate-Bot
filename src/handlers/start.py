from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        text=(
        "Welcome to Studymate Bot!\n\n"
        "Choose an option from the menu below."
        ), 
        reply_markup=main_menu,
    )
    