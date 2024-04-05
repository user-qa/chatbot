from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

user_on_start = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Shaxsiy Ma'lumotlar"),
            KeyboardButton("Foydalanuvchi qidirish")
        ]
    ], resize_keyboard=True
)


user_personal_info = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("usernameni o'zgartirish"),
            KeyboardButton("ismni o'zgartirish"),
            KeyboardButton("Ma'lumotlarni olish")
        ],
        [
            KeyboardButton("Orqaga")
        ]

    ], resize_keyboard=True
)