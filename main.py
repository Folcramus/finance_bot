import asyncio
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from bitrix_deals_report import create_deals_report
import logging

load_dotenv()
bot = Bot(token=os.getenv("FINANCE_TOKEN"))
dp = Dispatcher()

# 📄 Имя итогового PDF файла
REPORT_FILENAME = "bitrix_deals_report.pdf"

# 📌 Логирование
logging.basicConfig(level=logging.INFO)

# 📦 Инициализация бота и диспетчера
dp = Dispatcher()

# 📌 /start — стартовая команда
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Получить отчет", callback_data="get_report")]
    ])
    await message.answer("Привет! Нажми кнопку ниже, чтобы получить свежий отчет по сделкам:", reply_markup=keyboard)

# 📌 Обработка нажатия кнопки
@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "get_report":
        await callback_query.answer("⏳ Формирую отчет...")

        try:
            # 📄 Формируем отчет напрямую вызвав функцию
            create_deals_report(REPORT_FILENAME)

            # 📤 Отправляем PDF файл пользователю
            await bot.send_document(
                chat_id=callback_query.from_user.id,
                document=types.FSInputFile(REPORT_FILENAME)
            )

        except Exception as e:
            logging.error(f"Ошибка при формировании отчета: {e}")
            await bot.send_message(chat_id=callback_query.from_user.id, text="❌ Произошла ошибка при формировании отчета.")

# 📌 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
