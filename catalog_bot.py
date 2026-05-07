
@dp.callback_query(lambda c: c.data.startswith("chapter_"))
async def send_chapter(callback: types.CallbackQuery):
    msg_id = int(callback.data.replace("chapter_", ""))
    await bot.forward_message(chat_id=callback.message.chat.id,
                              from_chat_id=BOOKS_CHAT_ID,
                              message_id=msg_id)
    # сразу показываем кнопки возврата
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ К списку глав", callback_data="back_to_chapters")],
        [InlineKeyboardButton(text="🏠 Меню", callback_data="home")]
    ])
    await callback.message.answer("", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("movie_"))
async def send_movie(callback: types.CallbackQuery):
    msg_id = int(callback.data.replace("movie_", ""))
    await bot.copy_message(chat_id=callback.message.chat.id,
                           from_chat_id=MOVIES_CHAT_ID,
                           message_id=msg_id)
    # сразу показываем кнопки возврата
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ К списку фильмов", callback_data="back_to_movies")],
        [InlineKeyboardButton(text="🏠 Меню", callback_data="home")]
    ])
    await callback.message.answer("", reply_markup=keyboard)
















