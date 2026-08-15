from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


about_button = KeyboardButton(text="About")
future_features_button = KeyboardButton(text="Future Features")
notifications_button = KeyboardButton(text="Notifications")
back_button = KeyboardButton(text="Back")

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [about_button],
        [future_features_button],
        [notifications_button],
        [back_button],
    ],
    resize_keyboard=True,
)
