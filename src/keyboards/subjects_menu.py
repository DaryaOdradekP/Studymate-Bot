from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


add_button = KeyboardButton(text="Add Subject")
show_button = KeyboardButton(text="Show Subject")
delete_button = KeyboardButton(text="Delete Subject")
back_button = KeyboardButton(text="Back")

subjects_menu = ReplyKeyboardMarkup(
    keyboard=[
        [add_button, show_button],
        [delete_button, back_button],
    ],
    resize_keyboard=True,
)
