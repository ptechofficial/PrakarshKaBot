from typing import Final
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

# Commands
async def start_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Alright, tell me; What do you want to know about the great Prakarsh Gupta?")

async def help_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sure, just give me some gold and I shall help you")

async def custom_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")


# Web App

async def launch_web_ui(update: Update, callback: CallbackContext):
    kb = [ [KeyboardButton("Show me App!", web_app=WebAppInfo("https://ptechofficial.github.io/PrakarshKaBot/"))] ]
    await update.message.reply_text("Let's do this...", reply_markup=ReplyKeyboardMarkup(kb))

# Responses
def handle_response(text: str) -> str:
    processed:str = text.lower()

    if 'hi' in processed:
        return 'Aur bhai, kya haal chaal?'
    
    if 'who' in processed and 'prakarsh' in processed:
        return 'Prakarsh Gupta is a Software Developer Engineer at Expedia Group.'

    if 'where' in processed and {'prakarsh' or 'he'} in processed:
        return 'Prakarsh is currently based in India.'

    if 'work' in processed and {'prakarsh' or 'he'} in processed:
        return 'Prakarsh works at Expedia Group as a Software Developer Engineer.'

    if 'experience' in processed and {'prakarsh' or 'he'} in processed:
        return 'Prakarsh has extensive experience in software development, particularly in Python.'

    if 'skills' in processed and 'prakarsh' in processed:
        return 'Prakarsh is skilled in Python, Java, and various other programming languages.'

    if 'education' in processed and 'prakarsh' in processed:
        return 'Prakarsh has a degree in Computer Science.'

    if 'projects' in processed and 'prakarsh' in processed:
        return 'Prakarsh has worked on numerous projects, including developing this Telegram bot.'

    if 'hobbies' in processed and 'prakarsh' in processed:
        return 'When not coding, Prakarsh enjoys reading and playing video games.'

    if 'contact' in processed and 'prakarsh' in processed:
        return 'Sorry, I cannot provide contact information.'

    if 'salary' in processed and 'prakarsh' in processed:
        return 'Sorry, I cannot provide information about Prakarsh\'s salary.'

    return 'I do not understand what you wrote...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in ({message_type}) is sending ({text})')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text)
        else:
            return
    else:
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
    app.add_handler(CommandHandler('web_app', launch_web_ui))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3) # 3 seconds check
