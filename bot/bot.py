import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from settings import TELEGRAM_BOT_TOKEN

bot = Bot( token = TELEGRAM_BOT_TOKEN )
dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton(text="Кнопка 1", callback_data="btn1")
    button2 = types.InlineKeyboardButton(text="Кнопка 2", callback_data="btn2")

    keyboard.add(button1, button2)

    await message.answer("Здравствуйте, это проект Shaurmania!", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback(callback_query: types.CallbackQuery):
    code = callback_query.data
    if code == 'btn1:':
        await bot.answer_callback_query(callback_query.id, text="Кнопка 1")
    elif code == 'btn2':
        await bot.answer_callback_query(callback_query.id, text="Кнопка 2")

@dp.message(Command("test"))
async def command_test_handler(message: Message) -> None:
    await message.answer("Ну допустим я ответил и чё?")

# Run the bot
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
        