from loader import db, dp
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from states.user import ChangesState
from keyboards.default.user import user_personal_info

@dp.message_handler(text = "Shaxsiy Ma'lumotlar")
async def on_change_username(message: types.Message):
    await message.answer(text = 'Personal Data Section', reply_markup=user_personal_info)

@dp.message_handler(text = ["usernameni o'zgartirish"])
async def on_change_username(message: types.Message):
    text = "Yangi username kiriting! "
    await message.answer(text)

    await ChangesState.change_user.set()

@dp.message_handler(state=ChangesState.change_user)
async def change_username(message: types.Message, state: FSMContext):
    username = message.text
    if db.get_user_by_username(username.lower()):
        text = f'{username} allaqachon band qilingan'
        await message.answer(text)
        await ChangesState.change_user.set()
    else:
        await state.update_data(username=username.lower(), chat_id = message.chat.id)
        data = await state.get_data()
        db.update_username(data)
        await message.answer('Username changed✅')
        await state.finish()



@dp.message_handler(text = ["ismni o'zgartirish"])
async def on_change_username(message: types.Message):
    text = "Yangi ism kiriting! "
    await message.answer(text)

    await ChangesState.change_name.set()

@dp.message_handler(state=ChangesState.change_name)
async def change_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name.lower(), chat_id = message.chat.id)
    data = await state.get_data()
    db.update_name(data)
    await message.answer('Name changed✅')
    await state.finish()





@dp.message_handler(text=["Ma'lumotlarni olish"])
async def on_change_username(message: types.Message):
    current_user = db.get_user_by_chat_id(chat_id=message.chat.id)
    text = f""" Ismingiz:        {current_user[0][2]}
Usernamingiz:    {current_user[0][3]}
            """
    await message.answer(text = text)