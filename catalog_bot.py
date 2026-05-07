
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Конфигурация ---
BOT_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"
BOOKS_CHAT_ID = -1003979059214
MOVIES_CHAT_ID = -1003980018063

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Главное меню ---
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Аудиокниги", callback_data="books")],
        [InlineKeyboardButton(text="🎬 Фильмы", callback_data="movies")],
        [InlineKeyboardButton(text="🔄 Перезапуск", callback_data="restart")]
    ])

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

# --- Перезапуск ---
@dp.callback_query(lambda c: c.data == "restart")
async def restart_bot(callback: types.CallbackQuery):
    await callback.message.answer("🔄 Бот перезапущен!", reply_markup=main_menu())

# --- Аудиокниги ---
@dp.callback_query(lambda c: c.data == "books")
async def show_books(callback: types.CallbackQuery):
    # Здесь просто пример — можно расширить
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Пример книги", callback_data="book_1")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer("📖 Выберите книгу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("book_"))
async def show_chapters(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Глава 1", callback_data="chapter_1")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="books")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer("📖 Книга: Пример\nВыберите главу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("chapter_"))
async def send_chapter(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, "📖 Отправка главы...")

# --- Фильмы ---
@dp.callback_query(lambda c: c.data == "movies")
async def show_movies(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Пример фильма", callback_data="movie_1")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer("🎬 Выберите фильм:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("movie_"))
async def send_movie(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, "🎬 Отправка фильма...")

# --- Навигация ---
@dp.callback_query(lambda c: c.data == "back")
async def go_back(callback: types.CallbackQuery):
    await callback.message.answer("📚 Выберите категорию:", reply_markup=main_menu())

@dp.callback_query(lambda c: c.data == "home")
async def go_home(callback: types.CallbackQuery):
    await callback.message.answer("🏠 Главное меню:", reply_markup=main_menu())

# --- Запуск ---
async def main():
    print("✅ Бот запущен, ждём команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







