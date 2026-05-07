
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
import os

# --- Конфигурация ---
API_ID = int(os.getenv("API_ID", 30394715))
API_HASH = os.getenv("API_HASH", "81ee020c7e55609b24131f6e702237dd")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8793623384:AAH_Mh0b5xI7kEGKztlxgxnJmjBy9odjY8Q")

BOOKS_CHAT_ID = int(os.getenv("BOOKS_CHAT_ID", -1003979059214))
MOVIES_CHAT_ID = int(os.getenv("MOVIES_CHAT_ID", -1003980018063))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = TelegramClient("session_name", API_ID, API_HASH)

BOOKS = {}
MOVIES = {}

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

@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("📚 Выберите категорию:", reply_markup=main_menu())

# --- Перезапуск ---
@dp.callback_query(lambda c: c.data == "restart")
async def restart_bot(callback: types.CallbackQuery):
    await callback.message.answer("🔄 Бот перезапущен!", reply_markup=main_menu())

# --- Аудиокниги ---
@dp.callback_query(lambda c: c.data == "books")
async def show_books(callback: types.CallbackQuery):
    global BOOKS
    BOOKS = {}
    current_book = None
    book_index = 0

    async for msg in client.iter_messages(BOOKS_CHAT_ID, limit=200, reverse=True):
        if msg.text and msg.text.startswith("📚"):
            current_book = msg.text.replace("📚", "").strip()
            BOOKS[str(book_index)] = {"title": current_book, "chapters": []}
            book_index += 1
        elif current_book and msg.document:
            BOOKS[str(book_index-1)]["chapters"].append(msg.id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=data["title"], callback_data=f"book_{key}")]
        for key, data in BOOKS.items()
    ] + [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])

    await callback.message.answer("📖 Выберите книгу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("book_"))
async def show_chapters(callback: types.CallbackQuery):
    book_key = callback.data.replace("book_", "")
    book = BOOKS.get(book_key, {})
    chapters = book.get("chapters", [])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Глава {i+1}", callback_data=f"chapter_{book_key}_{msg_id}")]
        for i, msg_id in enumerate(chapters)
    ] + [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="books")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])

    await callback.message.answer(f"📖 Книга: {book.get('title','')}\nВыберите главу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("chapter_"))
async def send_chapter(callback: types.CallbackQuery):
    _, book_key, msg_id = callback.data.split("_", 2)
    msg_id = int(msg_id)
    await bot.forward_message(chat_id=callback.message.chat.id,
                              from_chat_id=BOOKS_CHAT_ID,
                              message_id=msg_id)

# --- Фильмы ---
@dp.callback_query(lambda c: c.data == "movies")
async def show_movies(callback: types.CallbackQuery):
    global MOVIES
    MOVIES = {}
    movie_index = 0
    async for msg in client.iter_messages(MOVIES_CHAT_ID, limit=50):
        if msg.video or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("video")):
            title = msg.text or f"Фильм {msg.id}"
            MOVIES[str(movie_index)] = {"title": title, "msg_id": msg.id}
            movie_index += 1

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=data["title"], callback_data=f"movie_{key}")]
        for key, data in MOVIES.items()
    ] + [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])

    await callback.message.answer("🎬 Выберите фильм:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("movie_"))
async def send_movie(callback: types.CallbackQuery):
    movie_key = callback.data.replace("movie_", "")
    movie = MOVIES.get(movie_key, {})
    msg_id = movie.get("msg_id")
    if msg_id:
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
    # Telethon только для чтения storage-чатов, без bot_token
    await client.connect()
    print("Бот запущен, ждём команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



