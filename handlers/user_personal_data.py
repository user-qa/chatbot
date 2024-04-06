from loader import db, dp
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from states.user import ChangesState
from keyboards.default.user import user_personal_info

@dp.message_handler(text = "Personal Information")
async def on_change_username(message: types.Message):
    await message.answer(text = 'Personal Information Section', reply_markup=user_personal_info)

@dp.message_handler(text = ["Change Username"])
async def on_change_username(message: types.Message):
    text = "Enter a new username!"
    await message.answer(text)

    await ChangesState.change_user.set()

@dp.message_handler(state=ChangesState.change_user)
async def change_username(message: types.Message, state: FSMContext):
    username = message.text
    not_allowed_char = 0
    if 5<=len(username) <= 32:
        for i in username:
            if i not in 'qwertyuioplkjhgfdsazxcvbnm1236547890_':
                not_allowed_char += 1
        if not_allowed_char == 0:
            if db.get_user_by_username(username.lower()):
                text = f'➡️{username}⬅️ has already been taken❗️'
                await message.answer(text)
                await ChangesState.change_user.set()
            else:
                await state.update_data(username=username.lower(), chat_id = message.chat.id)
                data = await state.get_data()
                db.update_username(data)
                await message.answer('Successfully Changed✅', reply_markup=user_personal_info)
                await state.finish()
        else:
            text = 'Invalid Username❗️'
            await message.answer(text)
            await ChangesState.change_user.set()
    else:
        text = 'Invalid Username❗\nLengths of the username must be between 5 and 32❗'
        await message.answer(text)
        await ChangesState.change_user.set()


@dp.message_handler(text = ["Change Full Name"])
async def on_change_username(message: types.Message):
    text = "Enter your full name! "
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





@dp.message_handler(text=["Get Personal Information"])
async def on_get_personal_info(message: types.Message):
    current_user = db.get_user_by_chat_id(chat_id=message.chat.id)
    text = f""" Your full name:     {current_user[0][2]}
Your username:    {current_user[0][3]}
            """
    await message.answer(text = text)
