import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
# /start command
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name

    keyboard = [
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
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Welcome, {user_name}!\n\nThanks for being a member of our channel🤝\n"
        "Follow Rolletto on our platforms and stay updated with the latest promotions, news, and rewards✨\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
    )

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
    app.add_error_handler(error_handler)

    logger.info("Bot is running...")
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())