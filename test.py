import json
import yaml
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler
import os
from test_function_calling import function_calling, hot_questions_gen

# Load environment variables
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('TOKEN_TEST')
BOT_USERNAME = os.getenv('USERNAME_TEST')

# Load messages from YAML
with open('meta_test.yaml', 'r',  encoding='utf-8') as file:
    messages = yaml.safe_load(file)['commands']

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = './Assets/Start.jpeg'

    reply_buttons = [
        [
            InlineKeyboardButton("Trade", callback_data='trade'),
            InlineKeyboardButton("Hot Questions", callback_data='hot_questions'),
        ],
        [
            InlineKeyboardButton("Portfolio", callback_data='portfolio'),
            InlineKeyboardButton("Earn", callback_data='earn'),
        ],
        [InlineKeyboardButton("Help", callback_data='help')],
    ]
    reply_button_markup = InlineKeyboardMarkup(reply_buttons)

    keyboard_buttons = [
        [InlineKeyboardButton("Hot Questions", callback_data='hot_questions')],
        [InlineKeyboardButton("Trade", callback_data='trade')],
        [InlineKeyboardButton("Portfolio", callback_data='portfolio')],
        [InlineKeyboardButton("Earn", callback_data='earn')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    keyboard_button_markup = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True)

    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(
            photo,
            caption=messages['start']['message'],
            reply_markup=keyboard_button_markup,
            parse_mode='HTML'
        )

    await update.message.reply_text(
        messages['start']['select_option'],
        reply_markup=reply_button_markup,
        parse_mode='HTML'
    )
    

async def hot_questions_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Earn", callback_data="earn"), InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = messages['hot_questions']['message']

    hot_questions_json = hot_questions_gen

    print(hot_questions_json)

    if update.callback_query: 
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')

async def trade_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Earn", callback_data="earn"), InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query: 
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text(messages['trade']['message'], reply_markup=reply_markup,
            parse_mode='HTML')
    else:
        await update.message.reply_text(messages['trade']['message'], reply_markup=reply_markup,
            parse_mode='HTML')

async def portfolio_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text(messages['portfolio']['message'],
            parse_mode='HTML')
    else:
        await update.message.reply_text(messages['portfolio']['message'],
            parse_mode='HTML')

async def earn_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text(messages['earn']['message'],
            parse_mode='HTML')
    else:
        await update.message.reply_text(messages['earn']['message'],
            parse_mode='HTML')

async def help_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text(messages['help']['message'],
            parse_mode='HTML')
    else:
        await update.message.reply_text(messages['help']['message'],
            parse_mode='HTML')


# Web App

async def launch_web_ui(update: Update, callback: CallbackContext):
    kb = [ [KeyboardButton("Show me App!", web_app=WebAppInfo("https://ptechofficial.github.io/PrakarshKaBot/"))] ]
    await update.message.reply_text(messages['webapp']['prompt'], reply_markup=ReplyKeyboardMarkup(kb),
            parse_mode='HTML')

async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    await update.message.reply_text(messages['webapp']['data_response'],
            parse_mode='HTML')
    for result in data:
        await update.message.reply_text(f"{result['name']}: {result['value']}")

async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    command = query.data
    await query.answer() 
    
    if command == "hot_questions":
        await hot_questions_command(update, context)
    elif command == "trade":
        await trade_command(update, context)
    elif command == "portfolio":
        await portfolio_command(update, context)
    elif command == "earn":
        await earn_command(update, context)
    elif command == "help":
        await help_command(update, context)


# Responses
def handle_response(text: str) -> str:
    processed:str = text.lower()
    print(f'Now executing, function_calling({text})')
    response_json = function_calling(processed)
    print(response_json.candidates[0].content.parts[0].text)
    return response_json.candidates[0].content.parts[0].text

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

    app.add_handler(CallbackQueryHandler(button_click))
    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('hot_questions', hot_questions_command))
    app.add_handler(CommandHandler('trade', trade_command))
    app.add_handler(CommandHandler('portfolio', portfolio_command))
    app.add_handler(CommandHandler('earn', earn_command))
    app.add_handler(CommandHandler('help', help_command))

    #Web App
    
    app.add_handler(CommandHandler('webapp', launch_web_ui))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    #Messages

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3) # 3 seconds check
