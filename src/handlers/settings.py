from aiogram import Router, F
from aiogram.types import Message

from src.database.settings import get_settings, set_notifications
from src.keyboards.main_menu import main_menu
from src.keyboards.settings_menu import settings_menu

router = Router()


@router.message(F.text == "Settings")
async def settings_handler(message: Message):
    await message.answer(
        text="Settings",
        reply_markup=settings_menu,
    )


@router.message(F.text == "About")
async def about_handler(message: Message):
    await message.answer(
        text=(
            "Studymate Bot\n\n"
            "Version: 1.0\n\n"
            "Technologies:\n"
            "• Python\n"
            "• aiogram\n"
            "• SQLite\n"
            "• SQLAlchemy\n\n"
            "Created by Darya Pavlova"
        )
    )


@router.message(F.text == "Future Features")
async def future_features_handler(message: Message):
    await message.answer(
        text=(
            "Planned features:\n\n"
            "• Task reminders\n"
            "• Task priority\n"
            "• Task filtering\n"
            "• Task sorting\n"
            "• Calendar integration"
        )
    )
    

@router.message(F.text == "Notifications")
async def notifications_handler(message: Message):
    user_id = message.from_user.id
    settings = get_settings(user_id)

    new_status = not settings.notifications_enabled

    set_notifications(user_id, new_status)

    status = "enabled" if new_status else "disabled"

    await message.answer(
        text=f"Notifications {status}."
    )


@router.message(F.text == "Back")
async def back_handler(message: Message):
    await message.answer(
        text="Main menu",
        reply_markup=main_menu,
    )
