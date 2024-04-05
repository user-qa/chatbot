from aiogram.dispatcher.filters.state import State, StatesGroup

class RegisterState(StatesGroup):
    full_name = State()
    username = State()

class ChangesState(StatesGroup):
    change_user = State()
    change_name = State()

class SearchState(StatesGroup):
    inputted_data = State()