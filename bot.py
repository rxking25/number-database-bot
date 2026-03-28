import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from database import search_user, create_db

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    exit(1)

create_db()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    welcome_text = """
🔍 *Number Database Pro Bot*

Welcome! Send me a Bangladeshi phone number like:
`8801838XXXXXX`

Type /cancel to abort.
    """
    
    keyboard = [
        [InlineKeyboardButton("📞 Search Number", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    help_text = """
*How to use:*
Send any Bangladeshi phone number starting with 880

*Number format:* 8801XXXXXXXXX
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("❌ Operation cancelled.")

async def validate_number(phone):
    pattern = r'^8801[3-9]\d{8}$'
    return bool(re.match(pattern, phone))

async def handle_number(update: Update, context: CallbackContext):
    phone = update.message.text.strip()
    
    if not await validate_number(phone):
        await update.message.reply_text(
            "❌ *Invalid number!*\n\nSend: `8801838XXXXXX`",
            parse_mode='Markdown'
        )
        return
    
    await update.message.reply_text("🔍 Looking up number... Please wait.")
    
    result = search_user(phone)
    
    if result:
        name, fb_id, points = result
        
        reply = f"""
🔍 *Number Lookup Result*

📱 *Number:* `{phone}`
👤 *Name:* {name}
📘 *Facebook ID:* {fb_id}

⭐ *Points left:* {points}
        """
        
        keyboard = [
            [InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone}")],
            [InlineKeyboardButton("📨 Telegram", url=f"https://t.me/{phone}")],
            [InlineKeyboardButton("🔄 Search Again", callback_data="search_again")],
        ]
        
        if fb_id != "Not Found":
            keyboard.insert(1, [InlineKeyboardButton("📘 Facebook", url=f"https://facebook.com/{fb_id}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode='Markdown')
        
    else:
        reply = f"""
❌ *Number Not Found*

Number: `{phone}`

Try another number.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data="search_again")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data == "search_again":
        await query.edit_message_text("📱 Send me another number:\n\nExample: `8801838XXXXXX`", parse_mode='Markdown')
    
    elif query.data == "help":
        help_text = """
*Commands:*
/start - Start
/help - Help
/cancel - Cancel

Send number: 8801XXXXXXXXX
        """
        await query.edit_message_text(help_text, parse_mode='Markdown')

async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    print("🤖 Bot is starting...")
    print(f"📱 Bot token: {TOKEN[:10]}...")
    
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
        print(f"🔗 Running with webhook: {webhook_url}")
        
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=webhook_url
        )
    else:
        print("🔄 Running with polling...")
        application.run_polling()

if __name__ == "__main__":
    main()
*Features:*
• Fast number lookup
• Name and Facebook ID information
• Direct WhatsApp & Telegram links
    """
    
    keyboard = [
        [InlineKeyboardButton("📞 Search Number", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👥 Share Bot", switch_inline_query="Check out this number lookup bot!")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    """হেল্প কমান্ড"""
    help_text = """
*How to use this bot:*

1. Send any Bangladeshi phone number starting with 880
2. Bot will search its database and show available information
3. Use the buttons below to:
   • Open WhatsApp chat
   • Open Telegram chat
   • Search another number
   • Share the bot with friends

*Number format:* `8801XXXXXXXXX`
*Example:* `8801838123456`

*Commands:*
/start - Start the bot
/help - Show this help
/cancel - Cancel current operation
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cancel(update: Update, context: CallbackContext):
    """ক্যান্সেল কমান্ড"""
    await update.message.reply_text("❌ Operation cancelled. Send /start to begin again.")

async def validate_number(phone):
    """ফোন নাম্বার ভ্যালিডেশন"""
    pattern = r'^8801[3-9]\d{8}$'
    return bool(re.match(pattern, phone))

async def handle_number(update: Update, context: CallbackContext):
    """ফোন নাম্বার হ্যান্ডলার"""
    phone = update.message.text.strip()
    
    # নাম্বার ভ্যালিডেশন
    if not await validate_number(phone):
        await update.message.reply_text(
            "❌ *Invalid number format!*\n\nPlease send a valid Bangladeshi number starting with 880\nExample: `8801838XXXXXX`",
            parse_mode='Markdown'
        )
        return
    
    # ওয়েটিং মেসেজ
    waiting_msg = await update.message.reply_text("🔍 Looking up number... Please wait.")
    
    # ডাটাবেজে খোঁজা
    result = search_user(phone)
    
    if result:
        name, fb_id, points = result
        
        reply = f"""
🔍 *Number Lookup Result*

📱 *Number:* `{phone}`
👤 *Name:* {name}
📘 *Facebook ID:* {fb_id}

⭐ *Points left:* {points}

*Quick Actions:*
        """
        
        # বাটন তৈরি
        keyboard = [
            [InlineKeyboardButton("💬 WhatsApp", url=f"https://wa.me/{phone}")],
            [InlineKeyboardButton("📨 Telegram", url=f"https://t.me/{phone}")],
            [InlineKeyboardButton("🔄 Search Again", callback_data="search_again")],
            [InlineKeyboardButton("📤 Share Bot", switch_inline_query="Check out this number lookup bot!")]
        ]
        
        # যদি Facebook ID থাকে তাহলে লিংক যোগ করি
        if fb_id != "Not Found":
            keyboard.insert(1, [InlineKeyboardButton("📘 Facebook", url=f"https://facebook.com/{fb_id}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await waiting_msg.delete()
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode='Markdown')
        
    else:
        await waiting_msg.delete()
        reply = f"""
❌ *Number Not Found*

Number: `{phone}`

This number is not in our database yet.

Try another number or check back later.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Try Another Number", callback_data="search_again")],
            [InlineKeyboardButton("📤 Share Bot", switch_inline_query="Check out this number lookup bot!")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(reply, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: CallbackContext):
    """বাটন ক্লিক হ্যান্ডলার"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "search_again":
        await query.edit_message_text("📱 Send me another Bangladeshi number:\n\nExample: `8801838XXXXXX`", parse_mode='Markdown')
    
    elif query.data == "help":
        help_text = """
*Number Database Pro Bot Help*

*Commands:*
/start - Start the bot
/help - Show this help message
/cancel - Cancel current operation

*How to use:*
Simply send a Bangladeshi phone number starting with 880 to get information.

*Number format:* 8801XXXXXXXXX
*Example:* 8801838123456

For support or feedback, contact @YourSupportHandle
        """
        await query.edit_message_text(help_text, parse_mode='Markdown')

async def error_handler(update: Update, context: CallbackContext):
    """এরর হ্যান্ডলার"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later or contact support."
        )

def main():
    """মেইন ফাংশন"""
    print("🤖 Bot is starting...")
    print(f"📱 Bot token: {8562581232:AAHBaABEWg40hibiwHdBRSP8m_M3y-wFkLE[:10]}...")
    
    application = Application.builder().token(8562581232:AAHBaABEWg40hibiwHdBRSP8m_M3y-wFkLE).build()
    
    # হ্যান্ডলার যোগ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)
    
    # Render এ Webhook বা Polling
    port = int(os.environ.get('PORT', 8443))
    app_url = os.environ.get("RENDER_EXTERNAL_URL")
    
    if app_url:
        # Webhook মোড (Render এর জন্য)
        webhook_url = f"{app_url}/{TOKEN}"
        print(f"🔗 Running with webhook: {webhook_url}")
        
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=webhook_url
        )
    else:
        # Polling মোড (লোকাল ডেভেলপমেন্টের জন্য)
        print("🔄 Running with polling...")
        application.run_polling()

if __name__ == "__main__":
    main()
