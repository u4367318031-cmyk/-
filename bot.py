import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8456685562:AAEsQgQH5TSy8oA2mxgywC3HJBYh_vykv0U"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Хранилище состояний игроков
users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {
        "wash": None,
        "clothes": None,
        "hair": None
    }

    keyboard = [
        [InlineKeyboardButton("Пенка", callback_data="wash_foam")],
        [InlineKeyboardButton("Мыло, которым моет голову", callback_data="wash_soap")]
    ]

    text = (
        "💖 Добро пожаловать в мемную игру про идеальное свидание!\n\n"
        "Главной героине нужно подготовиться к свиданию с Лупаменом.\n"
        "Для начала выбери, чем ей умыться:"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in users:
        users[user_id] = {
            "wash": None,
            "clothes": None,
            "hair": None
        }

    data = query.data

    # Шаг 1: умывание
    if data == "wash_foam":
        users[user_id]["wash"] = "foam"
        text = (
            "✨ Отличный выбор! Героиня умылась пенкой, кожа стала чистой и свежей.\n\n"
            "Теперь выбери наряд:"
        )
        keyboard = [
            [InlineKeyboardButton("Скини-штаны", callback_data="clothes_skinny")],
            [InlineKeyboardButton("Розовое платье с блёстками", callback_data="clothes_dress")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif data == "wash_soap":
        users[user_id]["wash"] = "soap"
        text = (
            "🫧 Ой... героиня умылась мылом не по назначению, и на лице появились прыщики.\n\n"
            "Теперь выбери наряд:"
        )
        keyboard = [
            [InlineKeyboardButton("Скини-штаны", callback_data="clothes_skinny")],
            [InlineKeyboardButton("Розовое платье с блёстками", callback_data="clothes_dress")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # Шаг 2: одежда
    elif data == "clothes_skinny":
        users[user_id]["clothes"] = "skinny"
        text = (
            "👖 Выбраны скини-штаны.\n\n"
            "Теперь выбери причёску:"
        )
        keyboard = [
            [InlineKeyboardButton("Распущенные волосы с локонами", callback_data="hair_curls")],
            [InlineKeyboardButton("Сальный пучок", callback_data="hair_bun")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif data == "clothes_dress":
        users[user_id]["clothes"] = "dress"
        text = (
            "👗 Выбрано красивое розовое платье с блёстками!\n\n"
            "Теперь выбери причёску:"
        )
        keyboard = [
            [InlineKeyboardButton("Распущенные волосы с локонами", callback_data="hair_curls")],
            [InlineKeyboardButton("Сальный пучок", callback_data="hair_bun")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # Шаг 3: причёска и финал
    elif data == "hair_curls":
        users[user_id]["hair"] = "curls"
        await show_result(query, user_id)
        return

    elif data == "hair_bun":
        users[user_id]["hair"] = "bun"
        await show_result(query, user_id)
        return


async def show_result(query, user_id):
    wash = users[user_id]["wash"]
    clothes = users[user_id]["clothes"]
    hair = users[user_id]["hair"]

    # Идеальная концовка
    if wash == "foam" and clothes == "dress" and hair == "curls":
        text = (
            "💘 Вы пришли на свидание с Лупаменом.\n\n"
            "Он в восторге: кожа сияет, платье шикарное, локоны прекрасны.\n"
            "Свидание прошло идеально!\n\n"
            "Лупамен говорит:\n"
            "«Ты выглядишь потрясающе... Давай встречаться?» 💍\n\n"
            "🎉 Победа! Идеальное свидание удалось!"
        )

    # Специальная плохая концовка
    elif wash == "soap" and clothes == "skinny" and hair == "bun":
        text = (
            "💔 Вы пришли на свидание с Лупаменом.\n\n"
            "Он посмотрел на твой образ и сказал:\n"
            "«Ну... сегодня ты выглядишь совсем не подготовленно к свиданию».\n\n"
            "Свидание прошло неловко.\n"
            "❌ Поражение!"
        )

    # Нейтральная концовка
    else:
        text = (
            "💞 Вы пришли на свидание с Лупаменом.\n\n"
            "Свидание прошло... неоднозначно. Некоторые детали образа получились удачно, "
            "а некоторые — не очень.\n\n"
            "Лупамен сказал:\n"
            "«Ты интересная, но можно было подготовиться получше».\n\n"
            "🔄 Это не идеальная концовка. Попробуй ещё раз и собери лучший образ!"
        )

    keyboard = [
        [InlineKeyboardButton("Начать заново", callback_data="restart")]
    ]

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def restart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    users[user_id] = {
        "wash": None,
        "clothes": None,
        "hair": None
    }

    keyboard = [
        [InlineKeyboardButton("Пенка", callback_data="wash_foam")],
        [InlineKeyboardButton("Мыло, которым моет голову", callback_data="wash_soap")]
    ]

    text = (
        "💖 Начинаем заново!\n\n"
        "Выбери, чем умыть главную героиню:"
    )

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(restart_handler, pattern="^restart$"))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
