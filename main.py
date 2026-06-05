from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from openai import AsyncOpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN")

if not OPENROUTER_API_KEY:
    raise ValueError("Не найден OPENROUTER_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

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

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот-помощник университета.\n\nВыбери раздел:",
        reply_markup=main_menu()
    )

@dp.message()
async def handle_text(message: types.Message):
    if not message.text:
        return

    text = message.text.lower()

    if "расписание" in text:
        await message.answer(
            "📅 Расписание:\nПн–Пт: 08:30 - 16:00"
        )

    elif "библиотека" in text:
        await message.answer(
            "📚 Библиотека:\n🕒 08:30 - 17:00"
        )

    elif "частые вопросы" in text:
        await message.answer(
            "❓ Частые вопросы:\n\n• Где находится деканат?\n• Как получить справку?\n• Как узнать расписание?"
        )

    elif "задать вопрос" in text:
        await message.answer(
            "✍️ Напишите ваш вопрос."
        )

    else:
        try:
            response = await client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты помощник университета. Отвечай кратко и по делу."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=300
            )

            answer = response.choices[0].message.content

            if answer:
                await message.answer(answer)
            else:
                await message.answer("Не удалось получить ответ.")

        except Exception as e:
            print(f"Ошибка OpenRouter: {e}")
            await message.answer("❌ Ошибка подключения к ИИ.")

async def main():
    print("🚀 Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
