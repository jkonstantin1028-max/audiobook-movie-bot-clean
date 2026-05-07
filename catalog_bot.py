
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8793623384:AAH_Mh0b5xI7kEGKztlxgxnJmjBy9odjY8Q"
BOOKS_CHAT_ID = -1003979059214
MOVIES_CHAT_ID = -1003980018063

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Конфигурация ---
books = {
    "Дневник леди Евы": (101, 124),
    "Вторая книга": (125, 137)
}

movies = {
    "Фильм 1": 7,
    "Фильм 2": 8,
    "Фильм 3": 9,
    "Фильм 4": 10,
    "Фильм 5": 11,
    "Фильм 6": 12,
    "Фильм 7": 13,
    "Фильм 8": 14,
    "Фильм 9": 15
}

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
    await callback.message.delete()  # удаляем старое сообщение
    await callback.message.answer("🔄 Бот перезапущен!", reply_markup=main_menu())

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
    start_id, end_id = books[title]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Глава {i}", callback_data=f"chapter_{msg_id}")]
        for i, msg_id in enumerate(range(start_id+1, end_id+1), start=1)
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

# --- Фильмы ---
@dp.callback_query(lambda c: c.data == "movies")
async def show_movies(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data=f"movie_{msg_id}")]
        for title, msg_id in movies.items()
    ] + [
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
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())











