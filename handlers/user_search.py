from loader import dp, db
from aiogram import types
from states.user import SearchState
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.user import user_on_start

@dp.message_handler(text = "Foydalanuvchi qidirish")
async def on_find_user(message: types.Message):
    text = 'Please, enter the username of the person you wanna search!'
    await message.answer(text = text)

    await SearchState.inputted_data.set()


@dp.message_handler(state = SearchState.inputted_data)
async def get_target_username(message:types.Message, state: FSMContext ):
    target_data_inputted = message.text
    target_full_data = db.get_user_by_username(target_data_inputted)
    if target_full_data:
        for person in target_full_data:
            text = f"Name: {person[2]}\n Username: {person[3]}"
            await message.answer(text)
    else:
        await message.answer(text="Ma'lumot topilmadi")
    await state.finish()


@dp.message_handler(text = "Orqaga")
async def on_find_user(message: types.Message):
    text = 'Went Back!'
    await message.answer(text = text, reply_markup=user_on_start)
