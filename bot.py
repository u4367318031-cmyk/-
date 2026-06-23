import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("8456685562:AAEsQgQH5TSy8oA2mxgywC3HJBYh_vykv0U")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {"role": None}

    keyboard = [
        [InlineKeyboardButton("Я девушка", callback_data="role_girl")],
        [InlineKeyboardButton("Я парень", callback_data="role_boy")]
    ]

    text = (
        "💘 Добро пожаловать в мемную игру «Найди парня или девушку»!\n\n"
        "Сначала выбери, кто ты:"
    )

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in users:
        users[user_id] = {"role": None}

    data = query.data

    if data == "role_girl":
        users[user_id]["role"] = "girl"
        keyboard = [
            [InlineKeyboardButton("Да, я такой 😎", callback_data="answer_boy_1")],
            [InlineKeyboardButton("Ты тоже ничего 😏", callback_data="answer_boy_2")]
        ]
        text = (
            "🌳 Ты гуляешь по парку и встречаешь будущую любовь.\n\n"
            "Перед тобой парень. Он говорит:\n"
            "«Ты такая интересная девушка...» 😍\n\n"
            "Что ответишь?"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "role_boy":
        users[user_id]["role"] = "boy"
        keyboard = [
            [InlineKeyboardButton("Ты чего такое говоришь? 😳", callback_data="answer_girl_1")],
            [InlineKeyboardButton("Ну и странное знакомство... 🙃", callback_data="answer_girl_2")]
        ]
        text = (
            "🌳 Ты гуляешь по парку и встречаешь будущую любовь.\n\n"
            "Перед тобой девушка. Она говорит:\n"
            "«Какой ты красивый мужчина!» 😍\n\n"
            "Что ответишь?"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data in ["answer_boy_1", "answer_boy_2"]:
        text = (
            "😱 Внезапно парень начинает странно светиться...\n\n"
            "Он превращается в Лупа-Залупу!\n"
            "Ты не успеваешь убежать, и он утаскивает тебя в мем-вселенную.\n\n"
            "🌀 Концовка: тебя забрал мем!"
        )
        keyboard = [[InlineKeyboardButton("Играть заново", callback_data="restart")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data in ["answer_girl_1", "answer_girl_2"]:
        text = (
            "😱 Внезапно девушка начинает странно светиться...\n\n"
            "Она превращается в Лупамена!\n"
            "Ты не успеваешь опомниться, и Лупамен утаскивает тебя в мем-вселенную.\n\n"
            "🌀 Концовка: тебя забрал мем!"
        )
        keyboard = [[InlineKeyboardButton("Играть заново", callback_data="restart")]]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "restart":
        users[user_id] = {"role": None}
        keyboard = [
            [InlineKeyboardButton("Я девушка", callback_data="role_girl")],
            [InlineKeyboardButton("Я парень", callback_data="role_boy")]
        ]
        text = (
            "💘 Начинаем заново!\n\n"
            "Выбери, кто ты:"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return


def main():
    if not TOKEN:
        raise ValueError("Не найден BOT_TOKEN в переменных окружения")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
