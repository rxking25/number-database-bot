import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from database import search_user, create_db

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("ERROR: BOT_TOKEN environment variable not set!")
    exit(1)

create_db()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    welcome_text = """
🔍 Number Database Pro Bot

Welcome! Send me a Bangladeshi phone number like:
8801838XXXXXX

Type /cancel to abort.
    """

    keyboard = [
        [InlineKeyboardButton("Search Number", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: CallbackContext):
    help_text = """
How to use:
Send any Bangladeshi phone number starting with 880

Number format: 8801XXXXXXXXX
    """
    await update.message.reply_text(help_text)

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")

async def validate_number(phone):
    pattern = r'^8801[3-9]\d{8}$'
    return bool(re.match(pattern, phone))

async def handle_number(update: Update, context: CallbackContext):
    phone = update.message.text.strip()

    if not await validate_number(phone):
        await update.message.reply_text(
            "Invalid number format!\n\nPlease send a valid Bangladeshi number starting with 880\nExample: 8801838XXXXXX"
        )
        return

    waiting_msg = await update.message.reply_text("Looking up number... Please wait.")

    result = search_user(phone)

    if result:
        name, fb_id, points = result

        reply = f"""
Number Lookup Result

Number: {phone}
Name: {name}
Facebook ID: {fb_id}

Points left: {points}
        """

        keyboard = [
            [InlineKeyboardButton("WhatsApp", url=f"https://wa.me/{phone}")],
            [InlineKeyboardButton("Telegram", url=f"https://t.me/{phone}")],
            [InlineKeyboardButton("Search Again", callback_data="search_again")],
        ]

        if fb_id != "Not Found":
            keyboard.insert(1, [InlineKeyboardButton("Facebook", url=f"https://facebook.com/{fb_id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await waiting_msg.delete()
        await update.message.reply_text(reply, reply_markup=reply_markup)

    else:
        await waiting_msg.delete()
        reply = f"""
Number Not Found

Number: {phone}

Try another number.
        """

        keyboard = [
            [InlineKeyboardButton("Try Again", callback_data="search_again")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(reply, reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "search_again":
        await query.edit_message_text("Send me another number:\n\nExample: 8801838XXXXXX")

    elif query.data == "help":
        help_text = """
Commands:
/start - Start
/help - Help
/cancel - Cancel

Send number: 8801XXXXXXXXX
        """
        await query.edit_message_text(help_text)

async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    print("Bot is starting...")
    print(f"Bot token: {TOKEN[:10]}...")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    port = int(os.environ.get('PORT', 8443))
    app_url = os.environ.get("RENDER_EXTERNAL_URL")

    if app_url:
        webhook_url = f"{app_url}/{TOKEN}"
        print(f"Running with webhook: {webhook_url}")

        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=webhook_url
        )
    else:
        print("Running with polling...")
        application.run_polling()

if __name__ == "__main__":
    main()
