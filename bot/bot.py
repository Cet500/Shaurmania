import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from settings import TELEGRAM_BOT_TOKEN

TOKEN = TELEGRAM_BOT_TOKEN

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")


@dp.message(Command("test"))
async def command_test_handler(message: Message) -> None:
    await message.answer("Ну допустим я ответил и чё?")

# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
        