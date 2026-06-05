from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from openai import AsyncOpenAI
import os

# ================= НАСТРОЙКИ =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# OpenRouter
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ================= МЕНЮ =================
def main_menu():
    kb = [
        [KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="📚 Библиотека")],
        [KeyboardButton(text="❓ Частые вопросы")],
        [KeyboardButton(text="✍️ Задать вопрос")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

# ================= START =================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-помощник университета.\n\nВыбери раздел:",
        reply_markup=main_menu()
    )

# ================= ОБРАБОТКА СООБЩЕНИЙ =================
@dp.message()
async def handle_text(message: types.Message):
    text = message.text.lower()

    if "расписание" in text:
        await message.answer(
            "📅 Расписание:\nПн–Пт: 8:30-16:00"
        )

    elif "библиотека" in text:
        await message.answer(
            "📚 Библиотека:\n🕒 08:30-17:00"
        )

    elif "вопрос" in text:
        await message.answer(
            "✍️ Задай свой вопрос:"
        )

    else:
        try:
            response = await client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты — помощник университета. Отвечай кратко и по делу."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=300
            )

            answer = response.choices[0].message.content
            await message.answer(answer)

        except Exception as e:
            print("Ошибка:", e)

            await message.answer(
                "❌ Ошибка подключения к ИИ."
            )

# ================= ЗАПУСК =================
async def main():
    print("🚀 Бот успешно запущен!")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
