from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


add_button = KeyboardButton(text="Add Task")
show_button = KeyboardButton(text="Show Tasks")
delete_button = KeyboardButton(text="Delete Task")
back_button = KeyboardButton(text="Back")

tasks_menu = ReplyKeyboardMarkup(
    keyboard=[
        [add_button, show_button],
        [delete_button, back_button],
    ],
    resize_keyboard=True,
)
