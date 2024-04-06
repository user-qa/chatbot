from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db
from states.user import RegisterState
from keyboards.default.user import user_on_start


@dp.message_handler(commands=['start'])
async def user_start(message: types.Message):
    current_user = db.get_user_by_chat_id(message.chat.id)
    if current_user:
        text = f'Hi, {current_user[0][2].title()}'
        await message.answer(text=text, reply_markup=user_on_start)
    else:
        text = 'Hi, enter your full name! '
        await message.answer(text)
        await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.lower()
    await state.update_data(chat_id=message.chat.id, full_name=full_name)
    text = f"{full_name.title()}, enter your username!"
    await message.answer(text)
    await RegisterState.username.set()


@dp.message_handler(state=RegisterState.username)
async def get_username(message: types.Message, state: FSMContext):
    username = message.text
    if 5 <= len(username) <= 32:
        for i in username:
            if i.isdigit() or i.isnumeric or i == '_':
                if db.get_user_by_username(username.lower()):
                    text = f'➡️{username}⬅️ has already been taken❗️'
                    await message.answer(text)
                    await RegisterState.username.set()
                else:
                    await state.update_data(username=username.lower())
                    data = await state.get_data()
                    db.add_user(data)
                    await message.answer('Successfully registered✅', reply_markup=user_on_start)
                    await state.finish()
            else:
                text = 'Invalid Username❗️'
                await message.answer(text)
                await RegisterState.username.set()
        else:
            text = 'Invalid Username❗\nLengths of the username must be between 5 and 32❗'
            await message.answer(text)
            await RegisterState.username.set()