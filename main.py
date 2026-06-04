from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import openai
import os

# ================= НАСТРОЙКИ =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Не установлены BOT_TOKEN или OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

openai.api_key = OPENAI_API_KEY

# Главное меню
def main_menu():
    kb = [
        [KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="📚 Библиотека")],
        [KeyboardButton(text="❓ Частые вопросы")],
        [KeyboardButton(text="✍️ Задать вопрос")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# ================= HANDLERS =================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-помощник университета.\n\nВыбери нужный раздел:", 
        reply_markup=main_menu()
    )

@dp.message()
async def handle_text(message: types.Message):
    text = message.text

    if text == "📅 Расписание":
        await message.answer("📌 Расписание занятий:\n\nПонедельник — Пятница\n08:00 - 16:00\n\nПодробное расписание [здесь](https://ecom).", parse_mode="Markdown")

    elif text == "📚 Библиотека":
        await message.answer("📚 Библиотека:\n\n🕒 Часы работы: 9:00 - 20:00\n\nЗапись книг — через сайт или лично.")

    elif text == "❓ Частые вопросы":
        await message.answer("❓ FAQ:\n\nНапиши свой вопрос ниже.")

    elif text == "✍️ Задать вопрос":
        await message.answer("✍️ Пиши свой вопрос:")

    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты — помощник университета. Отвечай кратко по темам: расписание, библиотека, учёба."},
                    {"role": "user", "content": text}
                ],
                max_tokens=600
            )
            await message.answer(response.choices[0].message.content)
        except:
            await message.answer("❌ Ошибка. Попробуй позже.")

# ================= ЗАПУСК =================
async def main():
    print("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
