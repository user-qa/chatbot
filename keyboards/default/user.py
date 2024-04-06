from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

user_on_start = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Personal Information"),
            KeyboardButton("Search Users")
        ]
    ], resize_keyboard=True
)


user_personal_info = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Change Username"),
            KeyboardButton("Change Full Name"),
            KeyboardButton("Get Personal Information")
        ],
        [
            KeyboardButton("Go Back")
        ]

    ], resize_keyboard=True
)