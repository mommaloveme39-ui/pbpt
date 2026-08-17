import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Your Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! The bot is now online and working!"
    )

# 🟢 NEW: This function handles regular text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # It simply repeats whatever the user typed back to them
    user_text = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"You said: {user_text}"
    )

async def main():
    # ⚠️ PASTE YOUR TOKEN HERE
    TOKEN = "8989884747:AAHurCrAEsDGx-d13hn8kp2jt930OobwEZ4"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add your command handlers
    application.add_handler(CommandHandler('start', start))
    
    # 🟢 NEW: Add a handler for all text messages (not starting with /)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot is starting...")
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    print("Bot is now running successfully!")
    
    # 🟢 Keep the bot alive on Render
    while True:
        # optional: you can remove the print if you want to clean up the logs
        print("Bot is alive and polling...")
        await asyncio.sleep(60)

# Runs the async function
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
