# Before calling this function make sure to install google generative ai package
# pip install -U -q google-generativeai

import pathlib
import textwrap
import time
import requests

import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
from IPython import display
from IPython.display import Markdown

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

available_queries = ['risingLiquidity','buyingPressure','solidPerformance','experiencedBuyers','riskyBets','blueChips','topGainers','topLosers', 'trending']


def call_discover_api(query:str):
  print(query)
  url = 'http://localhost:3000/api/discover'
  myobj = {'query': query}
  resp= requests.post(url, json = myobj)
  print(resp)
  return resp.text

def gen_response(functionPrompt:str):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',  tools=[call_discover_api])

    chat = model.start_chat(enable_automatic_function_calling=True)

    response = chat.send_message(functionPrompt)

    return response
 

def function_calling(userInput:str):
    
    message_template = """ 
    You have access to multiple APIs via the function "call_discover_api" which lets you pull data according to the user query. The function expects a string as a parameter. The string must be from this list: {available_queries}.
    We will ask questions like "Give me information about crypto having buying pressure." Follow the logic below:
    If only you're able to pick an appropriate string from the list that suits the question, then return the selected string and Send the response of the function by selecing these fields from the response:-token_name,token_symbol,price_usd,twitter_followers. Output the response in bullet pointwise manner, each bullet point describing a token in human readable plain english.
    If you cannot find a suitable string, return a reply according to your understanding. Make this reply very short. Very short.
    Here is the question: {user_input}
    """
    message = message_template.format(user_input=userInput, available_queries=available_queries)

    response = gen_response(message)
    return response

def hot_questions_gen():

    message_template = """ 
    I want you to return {available_queries} in 5 different texts
    """
    print("Hello world12")
    message = message_template.format(available_queries=available_queries)

    print(message)

    response = gen_response(message)
    return response