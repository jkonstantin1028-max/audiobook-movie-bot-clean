
import asyncio
from telethon import TelegramClient, events, Button
import os

API_ID = int(os.getenv("API_ID", 30394715))
API_HASH = os.getenv("API_HASH", "81ee020c7e55609b24131f6e702237dd")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8793623384:AAH_Mh0b5xI7kEGKztlxgxnJmjBy9odjY8Q")

BOOKS_CHAT_ID = int(os.getenv("BOOKS_CHAT_ID", -1003979059214))
MOVIES_CHAT_ID = int(os.getenv("MOVIES_CHAT_ID", -1003980018063))

client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

BOOKS = {}
MOVIES = {}

# --- Главное меню ---
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(
        "🏠 Главное меню:",
        buttons=[
            [Button.inline("📖 Аудиокниги", b"books")],
            [Button.inline("🎬 Фильмы", b"movies")],
            [Button.inline("🔄 Перезапуск", b"restart")]
        ]
    )

# --- Перезапуск ---
@client.on(events.CallbackQuery(data=b"restart"))
async def restart(event):
    await event.edit("🔄 Бот перезапущен!", buttons=[
        [Button.inline("📖 Аудиокниги", b"books")],
        [Button.inline("🎬 Фильмы", b"movies")]
    ])

# --- Аудиокниги ---
@client.on(events.CallbackQuery(data=b"books"))
async def show_books(event):
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

    buttons = [
        [Button.inline(data["title"], f"book_{key}".encode())]
        for key, data in BOOKS.items()
    ]
    buttons.append([Button.inline("⬅️ Назад", b"start")])
    await event.edit("📖 Выберите книгу:", buttons=buttons)

@client.on(events.CallbackQuery(pattern=b"book_"))
async def show_chapters(event):
    book_key = event.data.decode().replace("book_", "")
    book = BOOKS.get(book_key, {})
    chapters = book.get("chapters", [])

    buttons = [
        [Button.inline(f"Глава {i+1}", f"chapter_{book_key}_{msg_id}".encode())]
        for i, msg_id in enumerate(chapters)
    ]
    buttons.append([Button.inline("⬅️ Назад", b"books")])
    await event.edit(f"📖 Книга: {book.get('title','')}\nВыберите главу:", buttons=buttons)

@client.on(events.CallbackQuery(pattern=b"chapter_"))
async def send_chapter(event):
    _, book_key, msg_id = event.data.decode().split("_", 2)
    msg_id = int(msg_id)
    await client.forward_messages(event.chat_id, msg_id, BOOKS_CHAT_ID)

# --- Фильмы ---
@client.on(events.CallbackQuery(data=b"movies"))
async def show_movies(event):
    global MOVIES
    MOVIES = {}
    movie_index = 0
    async for msg in client.iter_messages(MOVIES_CHAT_ID, limit=50):
        if msg.video or (msg.document and msg.document.mime_type and msg.document.mime_type.startswith("video")):
            title = msg.text or f"Фильм {msg.id}"
            MOVIES[str(movie_index)] = {"title": title, "msg_id": msg.id}
            movie_index += 1

    buttons = [
        [Button.inline(data["title"], f"movie_{key}".encode())]
        for key, data in MOVIES.items()
    ]
    buttons.append([Button.inline("⬅️ Назад", b"start")])
    await event.edit("🎬 Выберите фильм:", buttons=buttons)

@client.on(events.CallbackQuery(pattern=b"movie_"))
async def send_movie(event):
    movie_key = event.data.decode().replace("movie_", "")
    movie = MOVIES.get(movie_key, {})
    msg_id = movie.get("msg_id")
    if msg_id:
        await client.forward_messages(event.chat_id, msg_id, MOVIES_CHAT_ID)

print("✅ Бот запущен...")
client.run_until_disconnected()




