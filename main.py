import json
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler
import os
from function_calling import function_calling
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('USERNAME')

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_path = './Assets/Start.jpeg'

    reply_buttons = [
        [
            InlineKeyboardButton("Whitelist", callback_data='whitelist'),
            InlineKeyboardButton("Trade", callback_data='trade'),
        ],
        [
            InlineKeyboardButton("Portfolio", callback_data='portfolio'),
            InlineKeyboardButton("Earn", callback_data='earn'),
        ],
        [InlineKeyboardButton("Support", callback_data='support')],
    ]
    reply_button_markup = InlineKeyboardMarkup(reply_buttons)

    keyboard_buttons = [
        [InlineKeyboardButton("Whitelist", callback_data='whitelist')],
        [InlineKeyboardButton("Trade", callback_data='trade')],
        [InlineKeyboardButton("Portfolio", callback_data='portfolio')],
        [InlineKeyboardButton("Earn", callback_data='earn')],
        [InlineKeyboardButton("Support", callback_data='support')]
    ]
    keyboard_button_markup = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True)


    with open(image_path, 'rb') as photo:
        await update.message.reply_photo(
            photo,
            caption="🌟 Welcome to Bella, your ultimate crypto news companion! 🌟 \nGet the latest updates, trade like a pro, and earn rewards! 💰📈 \n Explore the exciting world of cryptocurrencies with just a few clicks! 🚀\nNeed help? Our support team is always ready to assist you! 💬",
            reply_markup=keyboard_button_markup
        )

    await update.message.reply_text(
        "Select an option to proceed",
        reply_markup=reply_button_markup
    )
    

async def whitelist_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Earn", callback_data="earn"), InlineKeyboardButton("Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query: 
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text("🔒 Unlock exclusive benefits and join our whitelist today! 🔑\nStay tuned for more information on how to become a part of our elite community! 🌟👥\nGet ready for amazing perks and opportunities! 🎉🚀\n", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🔒 Unlock exclusive benefits and join our whitelist today! 🔑\nStay tuned for more information on how to become a part of our elite community! 🌟👥\nGet ready for amazing perks and opportunities! 🎉🚀\n", reply_markup=reply_markup)

async def trade_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Earn", callback_data="earn"), InlineKeyboardButton("Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query: 
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text("🎯 Ready to trade and conquer the crypto market? 🎯\nHead over to our cutting-edge webapp and unleash your trading potential! 📊💸\nExperience seamless trading like never before with Bella! 🌐🔒\n", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🎯 Ready to trade and conquer the crypto market? 🎯\nHead over to our cutting-edge webapp and unleash your trading potential! 📊💸\nExperience seamless trading like never before with Bella! 🌐🔒\n")

async def portfolio_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text("📜 Your Portfolio at Your Fingertips! 📜\nWith Bella, you can easily track and manage your cryptocurrency portfolio! 💼📊\n Stay on top of your investments and make informed decisions! 📈🎯\n")
    else:
        await update.message.reply_text("📜 Your Portfolio at Your Fingertips! 📜\nWith Bella, you can easily track and manage your cryptocurrency portfolio! 💼📊\n Stay on top of your investments and make informed decisions! 📈🎯\n")

async def earn_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text("💡 Want to earn while learning about cryptocurrencies? 💡\nBella offers incredible opportunities to boost your crypto earnings! 💪🌱\nStay tuned for exclusive promotions, giveaways, and rewards! 🎉🎁\n")
    else:
        await update.message.reply_text("💡 Want to earn while learning about cryptocurrencies? 💡\nBella offers incredible opportunities to boost your crypto earnings! 💪🌱\nStay tuned for exclusive promotions, giveaways, and rewards! 🎉🎁\n")

async def support_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 
        await update.callback_query.message.reply_text("🙋‍♂️ Need assistance? Our friendly support team is here for you! 🙋‍♀️\nWhether you have questions, concerns, or feedback, we're just a message away! 📩💬\nYour satisfaction is our top priority! 😊👍\n")
    else:
        await update.message.reply_text("🙋‍♂️ Need assistance? Our friendly support team is here for you! 🙋‍♀️\nWhether you have questions, concerns, or feedback, we're just a message away! 📩💬\nYour satisfaction is our top priority! 😊👍\n")


# Web App

async def launch_web_ui(update: Update, callback: CallbackContext):
    kb = [ [KeyboardButton("Show me App!", web_app=WebAppInfo("https://ptechofficial.github.io/PrakarshKaBot/"))] ]
    await update.message.reply_text("Let's do this...", reply_markup=ReplyKeyboardMarkup(kb))

async def web_app_data(update: Update, context: CallbackContext):
    data = json.loads(update.message.web_app_data.data)
    await update.message.reply_text("Your data was:")
    for result in data:
        await update.message.reply_text(f"{result['name']}: {result['value']}")

async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    command = query.data
    await query.answer() 
    
    if command == "whitelist":
        await whitelist_command(update, context)
    elif command == "trade":
        await trade_command(update, context)
    elif command == "portfolio":
        await portfolio_command(update, context)
    elif command == "earn":
        await earn_command(update, context)
    elif command == "support":
        await support_command(update, context)


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
    app.add_handler(CommandHandler('whitelist', whitelist_command))
    app.add_handler(CommandHandler('trade', trade_command))
    app.add_handler(CommandHandler('portfolio', portfolio_command))
    app.add_handler(CommandHandler('earn', earn_command))
    app.add_handler(CommandHandler('support', support_command))

    #Web App
    
    app.add_handler(CommandHandler('webapp', launch_web_ui))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    #Messages

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3) # 3 seconds check
