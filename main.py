from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from openai import AsyncOpenAI
import os

# ================= НАСТРОЙКИ =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

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
    await message.answer("👋 Привет! Я бот-помощник университета.\n\nВыбери раздел:", reply_markup=main_menu())

@dp.message()
async def handle_text(message: types.Message):
    text = message.text.lower()

    if "расписание" in text:
        await message.answer("📅 Расписание:\nПн–Пт: 10:00 - 17:30")
    elif "библиотека" in text:
        await message.answer("📚 Библиотека:\n🕒 09:00 - 20:00")
    elif "вопрос" in text:
        await message.answer("✍️ Задай свой вопрос:")
    else:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты — помощник университета. Отвечай кратко и по делу."},
                    {"role": "user", "content": text}
                ]
            )
            await message.answer(response.choices[0].message.content)
        except:
            await message.answer("❌ Нейронка сейчас не отвечает. Выбери кнопку из меню.")

async def main():
    print("🚀 Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
