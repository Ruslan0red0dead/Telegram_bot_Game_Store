from aiogram import Bot, types, Dispatcher, Router
import aiogram.utils.markdown as fmt
from game_api import Api_data
from keyboards import button
from config import TOKEN
from aiogram.filters import Command

# FSMContext, MemoryStorage, State, StatesGroup are needed to pass a list from one function to another
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

import asyncio
import logging
import sys

bot = Bot(token=TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)

class Form(StatesGroup):
    waiting_for_list = State()

# introduction
@dp.message(Command(commands=["start"]))
async def start_bot(message: types.Message):
    await message.answer('Enter the name of the game')

# this function will display a scrolling menu of games
@dp.message()
async def bot_send_message(message: types.Message, state: FSMContext):

    # is a replacement for the global function
    # to add data to the process_callback_button1 function

    my_list = Api_data(message.text)
    
    # save the list of games
    await state.set_state(Form.waiting_for_list)
    await state.update_data(my_list=my_list)

    index = len(my_list)

    try:
        await message.answer(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"1/{index}")
            )

    except IndexError:
        await message.answer('Game not found')

# button
@router.callback_query(lambda c: c.data in ['back', 'NEXT'])
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    user_data = await state.get_data()
    my_list = user_data.get('my_list')

    index = len(my_list)

    async def bot_keyboards():
        # 'callback_query.message.edit_text' is needed to change the displayed game in the list to the next game in the list 
        await callback_query.message.edit_text(
            fmt.text(
                'ㅤ',
                fmt.hide_link(my_list[0][1])
                ),
            parse_mode="HTML",
            reply_markup=button(my_list[0][1], f"{my_list[0][0]}/{index}")
            )

    if callback_query.data == 'NEXT':
        # this code adds a game from the beginning of the list to the end and adds a game from the end of the list to the beginning
        my_list.append(my_list[0])
        my_list.remove(my_list[0])
        await bot_keyboards()

    if callback_query.data == 'back':
        # this code works the other way around
        my_list.insert(0, my_list[-1])
        my_list.pop(index)
        await bot_keyboards()


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())