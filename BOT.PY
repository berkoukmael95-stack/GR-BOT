import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

# ================= CONFIG =================

TOKEN = os.getenv("8237102590:AAGlWSNkgyxOJdWmYvIYH8QdCcofvH8j9pU")  # token dans Railway
INVITE_LINK = os.getenv("https://t.me/+6zNWiAj71ic3MzY0")  # lien Telegram privé

# ==========================================

logging.basicConfig(level=logging.INFO)

captcha_answers = {}

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    a = random.randint(1, 9)
    b = random.randint(1, 9)

    captcha_answers[user.id] = a + b

    await update.message.reply_text(
        f"👋 Bonjour {user.first_name}\n\n"
        f"🔐 Pour accéder au canal, résous ce captcha :\n\n"
        f"👉 {a} + {b} = ?\n\n"
        f"✏️ Réponds uniquement avec le nombre."
    )

# ---------- Vérification ----------
async def check_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in captcha_answers:
        return

    try:
        answer = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Envoie uniquement un nombre.")
        return

    if answer == captcha_answers[user.id]:
        del captcha_answers[user.id]

        await update.message.reply_text(
            "✅ **Captcha validé !**\n\n"
            "🔓 Clique sur ce lien pour envoyer ta demande d’adhésion :\n"
            f"{INVITE_LINK}",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            "❌ Mauvaise réponse.\n"
            "🔁 Réessaie avec /start"
        )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_captcha))

    print("🤖 Bot lancé")
    app.run_polling()


if __name__ == "__main__":
    main()
