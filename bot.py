import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================================================
# CONFIGURATION
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
EXPERT_USERNAME = os.getenv("EXPERT_USERNAME", "Vibrantech1")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")

# Clean up username formatting automatically
EXPERT_USERNAME = EXPERT_USERNAME.replace("@", "").strip()

# Opens direct DM in-app for all users without web confirmation pop-ups
EXPERT_LINK = f"tg://resolve?domain={EXPERT_USERNAME}"


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# KEYBOARDS
# =========================================================

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔧 I Need Help With My Ads",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 What Can You Fix?",
                callback_data="services"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Common Ad Problems",
                callback_data="problems"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Contact Telegram Ads Expert",
                url=EXPERT_LINK
            )
        ],
    ])


def help_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔴 Ad Rejected / Declined",
                callback_data="rejected"
            )
        ],
        [
            InlineKeyboardButton(
                "🔗 Destination Problem",
                callback_data="destination"
            )
        ],
        [
            InlineKeyboardButton(
                "⚠️ Policy Problem",
                callback_data="policy"
            )
        ],
        [
            InlineKeyboardButton(
                "🔧 Other Telegram Ads Issue",
                callback_data="other"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Contact Expert",
                url=EXPERT_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="home"
            )
        ],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 Contact Expert",
                url=EXPERT_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="home"
            )
        ],
    ])


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    logger.info(
        "User started bot: %s (%s)",
        user.id,
        user.username
    )

    message = (
        "👋 Welcome to Telegram Ads Help.\n\n"
        "Having trouble getting your Telegram Ads approved?\n\n"
        "I help businesses and marketers troubleshoot "
        "Telegram Ads problems such as rejected or declined "
        "ads, destination issues and policy-related problems.\n\n"
        "👇 Select what you need help with:"
    )

    await update.message.reply_text(
        message,
        reply_markup=main_keyboard()
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "home":
        message = (
            "👋 Welcome to Telegram Ads Help.\n\n"
            "Having trouble getting your Telegram Ads approved?\n\n"
            "I help troubleshoot rejected, declined and "
            "problematic Telegram Ads.\n\n"
            "👇 Choose an option:"
        )
        await query.edit_message_text(
            message,
            reply_markup=main_keyboard()
        )

    elif action == "help":
        message = (
            "🔧 What problem are you experiencing?\n\n"
            "Choose the option that best describes your "
            "Telegram Ads problem."
        )
        await query.edit_message_text(
            message,
            reply_markup=help_keyboard()
        )

    elif action == "services":
        message = (
            "📋 What I Can Help With\n\n"
            "🔴 Rejected or declined Telegram Ads\n"
            "🔗 Destination-related problems\n"
            "⚠️ Policy and compliance issues\n"
            "📝 Ad copy problems\n"
            "🎯 Campaign setup troubleshooting\n"
            "🔍 Reviewing possible reasons for rejection\n\n"
            "For a proper review of your specific ad, "
            "contact me directly."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )

    elif action == "problems":
        message = (
            "❓ Common Telegram Ads Problems\n\n"
            "• Ad declined during review\n"
            "• Destination quality issues\n"
            "• Destination not functioning properly\n"
            "• Policy-related rejection\n"
            "• Ad text problems\n"
            "• Bot or channel destination issues\n\n"
            "The exact solution depends on the reason "
            "shown in your Telegram Ads account."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )

    elif action == "rejected":
        message = (
            "🔴 Ad Rejected / Declined\n\n"
            "If Telegram declined your ad, I can review "
            "the rejection reason and help identify what "
            "needs to be corrected.\n\n"
            "👉 Send me the rejected ad or screenshot of "
            "the rejection message in my DM."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )

    elif action == "destination":
        message = (
            "🔗 Destination Problem\n\n"
            "Telegram Ads destinations need to be functional, "
            "active and provide a proper user experience.\n\n"
            "If your ad is showing a destination-related "
            "error, send me the error message or screenshot "
            "so I can review it."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )

    elif action == "policy":
        message = (
            "⚠️ Policy Problem\n\n"
            "If your ad was declined because of a policy or "
            "content-related issue, send me the exact rejection "
            "message.\n\n"
            "I'll help you understand what needs to be "
            "changed before you resubmit."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )

    elif action == "other":
        message = (
            "🔧 Other Telegram Ads Issue\n\n"
            "No problem.\n\n"
            "Send me a screenshot of the problem and explain "
            "what happened. I'll take a look."
        )
        await query.edit_message_text(
            message,
            reply_markup=back_keyboard()
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while handling update:",
        exc_info=context.error
    )


# =========================================================
# MAIN
# =========================================================

def main():
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    logger.info("Telegram Ads bot is starting...")

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
