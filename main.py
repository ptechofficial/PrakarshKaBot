import json
import yaml
import re
import requests
import logging
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler
from gemini_calling import function_calling, hot_questions_gen
from bs4 import BeautifulSoup

# Load environment variables
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('USERNAME')

# Load messages from YAML
with open('test/meta_test.yaml', 'r',  encoding='utf-8') as file:
    messages = yaml.safe_load(file)['commands']

def is_valid_html(input_string: str) -> bool:
    try:
        soup = BeautifulSoup(input_string, 'html.parser')
        return bool(soup.find())
    except Exception:
        return False
    
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.callback_query):
        update = update.callback_query
    image_path = './Assets/start.jpg'

    reply_buttons = [
        [
            InlineKeyboardButton("Hot Questions", callback_data='hot_questions'),
        ],
    ]
    reply_button_markup = InlineKeyboardMarkup(reply_buttons)

    keyboard_buttons = [
        [InlineKeyboardButton("Start", callback_data='start'),
        InlineKeyboardButton("Hot Questions", callback_data='hot_questions')],
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

question_array = []

async def hot_questions_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
    hot_questions_json = hot_questions_gen()
    question_list_string = hot_questions_json.candidates[0].content.parts[0].text

    # Splitting and storing question_list_string to question_array
    html_pattern = re.compile(r'<[^>]+>')
    emoji_pattern = re.compile(r'[⭐\d\.]+')
    questions = question_list_string.strip().split('\n')
    question_array.clear() 

    for question in questions:
        clean_question = html_pattern.sub('', question).strip()
        clean_question = emoji_pattern.sub('', clean_question).strip()
        question_array.append(clean_question)

    print(question_array)

    keyboard = []
    inline_keyboard = []

    for index, question in enumerate(question_array, start=1):
        button_text = f"Q{index}"
        callback_data = str(index)
        inline_keyboard.append(InlineKeyboardButton(button_text, callback_data=callback_data))
    keyboard.append(inline_keyboard)

    reply_markup = InlineKeyboardMarkup(keyboard)

    title_message = messages['hot_questions']['message']
    question_template = messages['hot_questions']['template_questions']
    

    if update.callback_query: 
        await update.callback_query.answer() 
        update = update.callback_query    
        
    if is_valid_html(question_list_string):
        await update.message.reply_text(title_message + "\n" + question_list_string, parse_mode='HTML', reply_markup=reply_markup)
    else:
        await update.message.reply_text(title_message + "\n" +question_template, parse_mode='HTML', reply_markup=reply_markup)


async def news_command(update: Update, context = ContextTypes.DEFAULT_TYPE):
     # API URL
    url = "https://bella.thumbnailai.online/cryptoNews/trendingNews"  # Replace with your actual API URL

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Extract headlines from the JSON response
        headlines = [item.get("headline", "No headline found") for item in data]

        # Format the headlines into a single message
        reply_message = "\n".join(headlines)

        # Send the message to the user
        if update.callback_query:
            await update.callback_query.message.reply_text(reply_message, parse_mode='HTML')
        else:
            await update.message.reply_text(reply_message, parse_mode='HTML')

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        update.message.reply_text("Failed to fetch data from the API. Please try again later.")

async def response_with_buttons(update: Update, response: str):
    statements = response.strip().split('\n')
    statements = [statement.lstrip('#').strip() for statement in statements]

    for statement in statements:
        token_buttons = [
            [
                InlineKeyboardButton("Trade", url="https://bellawebapp-chandan867s-projects.vercel.app/charts"),
                InlineKeyboardButton("More Info", url="https://bellawebapp-chandan867s-projects.vercel.app/detailedReport"),
            ],
        ]
        token_button_markup = InlineKeyboardMarkup(token_buttons)
        if update.callback_query:
            await update.callback_query.message.reply_text(statement, parse_mode='HTML', reply_markup = token_button_markup)
        else:
            await update.message.reply_text(statement, parse_mode='HTML', reply_markup = token_button_markup)

async def hot_questions_response(update: Update):
    query = update.callback_query
    index = int(query.data) -1 
    question =question_array[index]
    response_json: json = fetch_response(question)
    
    if query.message:
        await query.message.reply_text(question)
    else:
        await update.message.reply_text(question)
    await response_with_buttons(update, response_json['message'])

async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    command = query.data
    await query.answer() 
    
    if command == "start":
        await start_command(query)
    elif command == "hot_questions":
        await hot_questions_command(update, context)
    else:   
        await hot_questions_response(update)

# Responses
def fetch_response(text: str) -> json:
    processed:str = text.lower()
    print(f'Now executing, function_calling({text})')
    response = function_calling(processed)
    response_json_str = response.candidates[0].content.parts[0].text
    
    response_json_str = response_json_str.replace('json', '')
    response_json_str = response_json_str.replace('```', '')

    print(f"Response json = {response_json_str}")
    response_json =json.loads( response_json_str)
    
    return response_json

async def general_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text

    print(f'User ({update.message.chat.id}) in ({message_type}) is sending ({text})')
    response_json: json = fetch_response(text)
    message = response_json['message']
    is_response = response_json['isResponse']
    if is_response:
        await response_with_buttons(update, message)
    else:
        await update.message.reply_text(message, parse_mode="HTML")

      
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'ERROR!   --  Update: ({update}) caused error: ({context.error})')

if __name__ == '__main__':
    
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CallbackQueryHandler(button_click))

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('hot_questions', hot_questions_command))
    app.add_handler(CommandHandler('news', news_command))


    #Messages
    app.add_handler(MessageHandler(filters.TEXT, general_response))

    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=1) # 3 seconds check
