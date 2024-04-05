from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loader import dp, db
from states.user import RegisterState
from keyboards.default.user import user_on_start


@dp.message_handler(commands=['start'])
async def user_start(message: types.Message):
    current_user = db.get_user_by_chat_id(message.chat.id)
    if current_user:
        text = f'Assalomu alaykum, {current_user[0][2].title()}'
        await message.answer(text=text, reply_markup=user_on_start)
    else:
        text = 'Assalomu alaykum, ismingizni kiriting! '
        await message.answer(text)
        await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text.lower()
    await state.update_data(chat_id=message.chat.id, full_name=full_name)
    text = f"{full_name.title()}, iltimos username kiriting"
    await message.answer(text)
    await RegisterState.username.set()


@dp.message_handler(state=RegisterState.username)
async def get_username(message: types.Message, state: FSMContext):
    username = message.text
    if db.get_user_by_username(username.lower()):
        text = f'{username} allaqachon band qilingan'
        await message.answer(text)
        await RegisterState.username.set()
    else:
        await state.update_data(username=username.lower())
        data = await state.get_data()
        db.add_user(data)
        await message.answer('Successfully registered✅')
        await state.finish()
