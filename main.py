import json
from typing import Final
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler
import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('USERNAME')

# Commands
async def start_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Whitelist"), KeyboardButton("Trade")],
        [KeyboardButton("Portfolio"), KeyboardButton("Earn")],
        [KeyboardButton("Support")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Storm Trade - first leveraged DEX on TON! ⚡️ \n\n To start your trading journey, open app and connect your TON wallet 👇", reply_markup=reply_markup)

async def whitelist_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected the Whitelist command.")

async def trade_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Earn", callback_data="/earn"), InlineKeyboardButton("Support", callback_data="/support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("You selected the TRADE command.", reply_markup=reply_markup)

async def portfolio_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected the PORTFOLIO command.")

async def earn_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected the EARN command.")

async def support_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You selected the SUPPORT command.")


# Web App

async def launch_web_ui(update: Update, callback: CallbackContext):
    kb = [ [KeyboardButton("Show me App!", web_app=WebAppInfo("https://ptechofficial.github.io/PrakarshKaBot/"))] ]
    await update.message.reply_text("Let's do this...", reply_markup=ReplyKeyboardMarkup(kb))

async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    await update.message.reply_text("Your data was:")
    for result in data:
        await update.message.reply_text(f"{result['name']}: {result['value']}")

# Responses
def handle_response(text: str) -> str:
    processed:str = text.lower()
    return processed

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in ({message_type}) is sending ({text})')

    response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'ERROR!   --  Update: ({update}) caused error: ({context.error})')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('whitelist', whitelist_command))
    app.add_handler(CommandHandler('trade', trade_command))
    app.add_handler(CommandHandler('portfolio', portfolio_command))
    app.add_handler(CommandHandler('earn', earn_command))
    app.add_handler(CommandHandler('support', support_command))

    #Web App
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3) # 3 seconds check
