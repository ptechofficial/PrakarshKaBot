import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
import telegram.ext
import random

# Retrieve token from environment variables
TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

# List of random two-line messages
messages = [
    "Welcome to our trading bot!\nHow can I assist you today?",
    "Hello! Ready to start trading?\nSelect an option below to begin.",
    "Hi there!\nWhat would you like to do today?",
    "Greetings!\nChoose an option to proceed.",
]

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    random_message = random.choice(messages)
    keyboard = [
        [InlineKeyboardButton("Trade", callback_data='trade'), InlineKeyboardButton("Portfolio", callback_data='portfolio')],
        [InlineKeyboardButton("Earn", callback_data='earn'), InlineKeyboardButton("Support", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(random_message, reply_markup=reply_markup)

# Function to handle Trade button
def trade(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='start'), InlineKeyboardButton("Google", url='https://google.com')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Trade selected.\nChoose an option:", reply_markup=reply_markup)

# Function to handle Portfolio button
def portfolio(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Start Over", callback_data='start'), InlineKeyboardButton("Google", url='https://google.com')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Portfolio selected.\nChoose an option:", reply_markup=reply_markup)

# Function to handle Earn button
def earn(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Start Over", callback_data='start'), InlineKeyboardButton("Google", url='https://google.com')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Earn selected.\nChoose an option:", reply_markup=reply_markup)

# Function to handle Support button
def support(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Start Over", callback_data='start'), InlineKeyboardButton("Google", url='https://google.com')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Support selected.\nChoose an option:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'start':
        start(update, context)
    elif query.data == 'trade':
        trade(update, context)
    elif query.data == 'portfolio':
        portfolio(update, context)
    elif query.data == 'earn':
        earn(update, context)
    elif query.data == 'support':
        support(update, context)

def set_commands(dispatcher: Dispatcher) -> None:
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("trade", "Access trading options"),
        BotCommand("portfolio", "View your portfolio"),
        BotCommand("earn", "Learn how to earn"),
        BotCommand("support", "Get support"),
    ]
    dispatcher.bot.set_my_commands(commands)

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Set commands for the bot
    set_commands(dispatcher)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
