from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


subjects_button = KeyboardButton(text="Subjects")
tasks_button = KeyboardButton(text="Tasks")
statistics_button = KeyboardButton(text="Statistics")
settings_button = KeyboardButton(text="Settings")

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [subjects_button],
        [tasks_button],
        [statistics_button],
        [settings_button],
    ],
    resize_keyboard=True,
)
