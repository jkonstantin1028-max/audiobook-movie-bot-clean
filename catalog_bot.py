
import asyncio, json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8793623384:AAH_Mh0b5xI7kEGKztlxgxnJmjBy9odjY8Q"
BOOKS_CHAT_ID = -1003979059214
MOVIES_CHAT_ID = -1003980018063

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Загружаем книги
with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Аудиокниги", callback_data="books")],
        [InlineKeyboardButton(text="🎬 Фильмы", callback_data="movies")],
        [InlineKeyboardButton(text="🔄 Перезапуск", callback_data="restart")]
    ])

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

# --- Книги ---
@dp.callback_query(lambda c: c.data == "books")
async def show_books(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data=f"book_{title}")]
        for title in books.keys()
    ] + [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer("📖 Выберите книгу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("book_"))
async def show_chapters(callback: types.CallbackQuery):
    title = callback.data.replace("book_", "")
    chapters = books[title]["chapters"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Глава {i+1}", callback_data=f"chapter_{msg_id}")]
        for i, msg_id in enumerate(chapters)
    ] + [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="books")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer(f"📖 {title}\nВыберите главу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("chapter_"))
async def send_chapter(callback: types.CallbackQuery):
    msg_id = int(callback.data.replace("chapter_", ""))
    await bot.forward_message(chat_id=callback.message.chat.id,
                              from_chat_id=BOOKS_CHAT_ID,
                              message_id=msg_id)

# --- Фильмы (аналогично, можно сделать movies.json) ---
@dp.callback_query(lambda c: c.data == "movies")
async def show_movies(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Фильм 1", callback_data="movie_301")],
        [InlineKeyboardButton(text="🎬 Фильм 2", callback_data="movie_302")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])
    await callback.message.answer("🎬 Выберите фильм:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("movie_"))
async def send_movie(callback: types.CallbackQuery):
    msg_id = int(callback.data.replace("movie_", ""))
    await bot.copy_message(chat_id=callback.message.chat.id,
                           from_chat_id=MOVIES_CHAT_ID,
                           message_id=msg_id)

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








