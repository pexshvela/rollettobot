import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------------------------------------------------------------------
# Load .env file for local development
# On Railway, environment variables are set directly in the dashboard
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration – reads BOT_TOKEN from .env file or Railway environment
# ---------------------------------------------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# ---------------------------------------------------------------------------
# Welcome messages per language
# ---------------------------------------------------------------------------
WELCOME_MESSAGES = {
    "en": (
        "Welcome, {name}!\n\n"
        "Thanks for being a member of our channel 🤝\n"
        "Follow Rolletto on our platforms and stay updated with the latest promotions, news, and rewards ✨\n\n"
        "Choose an option below:"
    ),
    "es": (
        "¡Bienvenido, {name}!\n\n"
        "Gracias por ser miembro de nuestro canal 🤝\n"
        "Sigue a Rolletto en nuestras plataformas y mantente al día con las últimas promociones, noticias y recompensas ✨\n\n"
        "Elige una opción a continuación:"
    ),
    "fr": (
        "Bienvenue, {name}!\n\n"
        "Merci d'être membre de notre chaîne 🤝\n"
        "Suivez Rolletto sur nos plateformes et restez informé des dernières promotions, actualités et récompenses ✨\n\n"
        "Choisissez une option ci-dessous:"
    ),
    "it": (
        "Benvenuto, {name}!\n\n"
        "Grazie per essere un membro del nostro canale 🤝\n"
        "Segui Rolletto sulle nostre piattaforme e rimani aggiornato con le ultime promozioni, notizie e premi ✨\n\n"
        "Scegli un'opzione qui sotto:"
    ),
}

# ---------------------------------------------------------------------------
# Inline buttons per language
# ---------------------------------------------------------------------------
KEYBOARDS = {
    "en": [
        [
            InlineKeyboardButton("𝕏 Follow X", url="https://x.com/RollettoWorld"),
            InlineKeyboardButton("🎮 Join Discord", url="https://discord.gg/eZzy3HEgus"),
        ],
        [
            InlineKeyboardButton("📸 Follow Instagram", url="https://www.instagram.com/rollettospace/"),
            InlineKeyboardButton("🎰 Play Now!", url="https://rolletto.space/rollettoworldbot"),
        ],
        [
            InlineKeyboardButton("👉 Join Telegram!", url="https://t.me/+-KV8UEJFcv9jMDIy"),
        ],
    ],
    "es": [
        [
            InlineKeyboardButton("𝕏 Seguir X", url="https://x.com/RollettoWorld"),
            InlineKeyboardButton("🎮 Unirse a Discord", url="https://discord.gg/eZzy3HEgus"),
        ],
        [
            InlineKeyboardButton("📸 Seguir Instagram", url="https://www.instagram.com/rollettospace/"),
            InlineKeyboardButton("🎰 ¡Jugar Ahora!", url="https://rolletto.space/rollettoworldbot"),
        ],
        [
            InlineKeyboardButton("👉 ¡Unirse a Telegram!", url="https://t.me/+-KV8UEJFcv9jMDIy"),
        ],
    ],
    "fr": [
        [
            InlineKeyboardButton("𝕏 Suivre X", url="https://x.com/RollettoWorld"),
            InlineKeyboardButton("🎮 Rejoindre Discord", url="https://discord.gg/eZzy3HEgus"),
        ],
        [
            InlineKeyboardButton("📸 Suivre Instagram", url="https://www.instagram.com/rollettospace/"),
            InlineKeyboardButton("🎰 Jouer Maintenant!", url="https://rolletto.space/rollettoworldbot"),
        ],
        [
            InlineKeyboardButton("👉 Rejoindre Telegram!", url="https://t.me/+-KV8UEJFcv9jMDIy"),
        ],
    ],
    "it": [
        [
            InlineKeyboardButton("𝕏 Segui X", url="https://x.com/RollettoWorld"),
            InlineKeyboardButton("🎮 Unisciti a Discord", url="https://discord.gg/eZzy3HEgus"),
        ],
        [
            InlineKeyboardButton("📸 Segui Instagram", url="https://www.instagram.com/rollettospace/"),
            InlineKeyboardButton("🎰 Gioca Ora!", url="https://rolletto.space/rollettoworldbot"),
        ],
        [
            InlineKeyboardButton("👉 Unisciti a Telegram!", url="https://t.me/+-KV8UEJFcv9jMDIy"),
        ],
    ],
}

# ---------------------------------------------------------------------------
# /start command – show language selection first
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="botlang_en"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="botlang_es"),
        ],
        [
            InlineKeyboardButton("🇫🇷 Français", callback_data="botlang_fr"),
            InlineKeyboardButton("🇮🇹 Italiano", callback_data="botlang_it"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🇬🇧 Hello!\n"
        "🇪🇸 ¡Hola!\n"
        "🇫🇷 Bonjour!\n"
        "🇮🇹 Ciao!\n\n"
        "Please choose your language / Elige tu idioma / Choisissez la langue / Scegli la lingua:",
        reply_markup=reply_markup,
    )

# ---------------------------------------------------------------------------
# Callback handler – language button pressed
# ---------------------------------------------------------------------------
async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_name = update.effective_user.first_name
    lang = query.data.replace("botlang_", "")  # "botlang_en" → "en"

    welcome_text = WELCOME_MESSAGES[lang].format(name=user_name)
    reply_markup = InlineKeyboardMarkup(KEYBOARDS[lang])

    await query.edit_message_text(
        text=welcome_text,
        reply_markup=reply_markup,
    )

    logger.info("User %s chose language: %s", update.effective_user.id, lang)

# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------
async def error_handler(update, context):
    logger.error("Error: %s", context.error)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern="^botlang_"))
    app.add_error_handler(error_handler)
    logger.info("Bot is running...")
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
