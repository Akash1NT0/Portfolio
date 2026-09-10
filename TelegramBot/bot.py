import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    age = State()

@dp.message(Command("reg"))
async def start_reg(message: types.Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def get_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"{data['name']}, {message.text} лет. Записал!")
    await state.clear()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я эхо-бот. Напиши что-нибудь, и я повторю."
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Просто напиши мне любое сообщение.")


@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сайт", url="https://telegram.org")],
        [InlineKeyboardButton(text="Нажми меня", callback_data="click")],
    ])
    await message.answer("Выбери:", reply_markup=kb)


@dp.callback_query(F.data == "click")
async def on_click(callback: types.CallbackQuery):
    await callback.answer("Ты нажал кнопку!")
    await callback.message.answer("Спасибо за клик 👍")


@dp.message(Command("keyboard"))
async def show_kb(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Привет")], [KeyboardButton(text="Пока")]],
        resize_keyboard=True,
    )
    await message.answer("Выбери кнопку:", reply_markup=kb)


@dp.message(Command("hide"))
async def hide_kb(message: types.Message):
    await message.answer("Клавиатура убрана", reply_markup=ReplyKeyboardRemove())


@dp.message(F.text == "Привет")
async def hello(message: types.Message):
    await message.answer("И тебе привет!")


@dp.message(F.text == "Пока")
async def bye(message: types.Message):
    await message.answer("До встречи!")


@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())