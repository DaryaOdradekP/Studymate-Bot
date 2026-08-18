from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


add_button = KeyboardButton(text="Add Task")
show_button = KeyboardButton(text="Show Tasks")
delete_button = KeyboardButton(text="Delete Task")
back_button = KeyboardButton(text="Back")
complete_button = KeyboardButton(text="Complete Task")
edit_button = KeyboardButton(text="Edit Task")
overdue_button = KeyboardButton(text="Overdue Tasks")
upcoming_button = KeyboardButton(text="Upcoming Tasks")
no_deadline_button = KeyboardButton(text="No Deadline Tasks")

tasks_menu = ReplyKeyboardMarkup(
    keyboard=[
        [add_button, show_button],
        [delete_button, complete_button],
        [edit_button, overdue_button],
        [upcoming_button, no_deadline_button],
        [back_button],
    ],
    resize_keyboard=True,
)
