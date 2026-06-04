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
    await message.answer(
        "👋 Привет! Я бот-помощник университета.\n\nВыбери раздел:", 
        reply_markup=main_menu()
    )

@dp.message()
async def handle_text(message: types.Message):
    text = message.text.lower()

    if "расписание" in text or text == "📅 расписание":
        await message.answer("📌 Расписание занятий:\n\nПн–Пт: 10:00 - 17:30\n\nПодробное расписание по группам — в сообщении ниже.")

    elif "библиотека" in text or text == "📚 библиотека":
        await message.answer("📚 Библиотека:\n\nЧасы работы: 09:00 - 20:00\nЗапись и продление — через сайт или лично.")

    elif "вопросы" in text or text == "❓ частые вопросы":
        await message.answer("❓ Частые вопросы:\nНапиши свой вопрос ниже.")

    elif "задать вопрос" in text or text == "✍️ задать вопрос":
        await message.answer("✍️ Задай свой вопрос:")

    else:
        # Ответ через ChatGPT
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты — дружелюбный помощник университета. Отвечай коротко и по делу по темам: расписание, библиотека, учёба."},
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            await message.answer(response.choices[0].message.content)
        except Exception as e:
            await message.answer("❌ Ошибка соединения с ИИ. Попробуй позже или выбери кнопку из меню.")

# ================= ЗАПУСК =================
async def main():
    print("🚀 Бот запущен успешно!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
