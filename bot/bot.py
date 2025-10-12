import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from settings import TELEGRAM_BOT_TOKEN

bot = Bot(token=str(TELEGRAM_BOT_TOKEN))
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    button_catalog = types.InlineKeyboardButton(text="Каталог", callback_data="catalog")
    button_site = types.InlineKeyboardButton(text="Перейти на сайт", url="https://shaurmaniaexample.ru")
    button_discount = types.InlineKeyboardButton(text="Скидки", callback_data="discounts")
    button_cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")
    button_orders = types.InlineKeyboardButton(text="Заказы", callback_data="orders")
    button_empty = types.InlineKeyboardButton(text="", callback_data="empty")

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [button_catalog, button_site],
            [button_discount, button_cart],
            [button_orders, button_empty]
        ]
    )

    photo_path = "media/user_images/Bilya_Herrington.jpg"  # путь к фото
    photo = types.FSInputFile(photo_path)
    await message.answer_photo(photo, caption="Здравствуйте, это проект Shaurmania!", reply_markup=keyboard)

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    code = callback_query.data
    if callback_query.message:
        if code == 'catalog':
            await callback_query.message.answer("Открыт каталог!")
        elif code == 'discounts':
            await callback_query.message.answer("Тут будут скидки!")
        elif code == 'cart':
            await callback_query.message.answer("Ваша корзина пуста!")
        elif code == 'orders':
            await callback_query.message.answer("Ваши заказы!")
        elif code == 'empty':
            await callback_query.message.answer("Пустая кнопка!")
    await callback_query.answer()

@dp.message(Command("test"))
async def command_test_handler(message: Message) -> None:
    await message.answer("Ну допустим я ответил и чё?")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
        