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

GEMINI_API_KEY = 'AIzaSyBByajzdb7tNcIFD8IEBJ0kZ9GKTfTBTu4'

genai.configure(api_key=GEMINI_API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def call_discover_api(query:str):
  print(query)
  # url = 'http://localhost:3000/api/discover'
  # myobj = {'query': query}
  # resp= requests.post(url, json = myobj)
  resp = "call_discover_api called with " + query
  print(resp)
  return resp
 

def function_calling(userInput:str):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash',  tools=[call_discover_api])

    chat = model.start_chat(enable_automatic_function_calling=True)

    # message_template = """ 
    # You have access to multiple APIs via the function "call_discover_api" which lets you pull data according to the user query. The function expects a string as a parameter. The string must be from this list: ['risingLiquidity','buyingPressure','solidPerformance','experiencedBuyers','riskyBets','blueChips','topGainers','topLosers','trending'].
    # We will ask questions like give me information about crypto having buying pressure. You need to pick the appropriate string from the list and pass it as a parameter to the given function. Send the response of the function by selecing these fields from the response:-token_name,token_symbol,price_usd,twitter_followers. Output the response in bullet pointwise manner, each bullet point describing a token in human readable plain english. 
    # Here is the question: {user_input}
    # """
    available_queries = ['risingLiquidity','buyingPressure','solidPerformance','experiencedBuyers','riskyBets','blueChips','topGainers','topLosers','trending']
 
    # message_template = """ 
    # If the question isn't widely related to crytpocurrencies or blockchain , reply with a friendly message asking the user to ask about cryptocurrency and don't proceed further.
    # Else you have access to multiple APIs via the function "call_discover_api" which lets you pull data according to the user query. The function expects a string as a parameter. The string must be from this list: {available_queries}.
    # We will ask questions like "Give me information about crypto having buying pressure." Follow the logic below:
    # If you're able to pick an appropriate string from the list that suits the question, then return the selected string.
    # If you cannot find a suitable string, return the most optimal solution using your knowledge.
    # Here is the question: {user_input}
    # """
    message_template = """ 
    You have access to multiple APIs via the function "call_discover_api" which lets you pull data according to the user query. The function expects a string as a parameter. The string must be from this list: {available_queries}.
    We will ask questions like "Give me information about crypto having buying pressure." Follow the logic below:
    If you're able to pick an appropriate string from the list that suits the question, then return the selected string and Send the response of the function by selecing these fields from the response:-token_name,token_symbol,price_usd,twitter_followers. Output the response in bullet pointwise manner, each bullet point describing a token in human readable plain english.
    If you cannot find a suitable string, return the most optimal solution using your knowledge. Make this reply very short. Very short.
    Here is the question: {user_input}
    """
    # Use the user input to fill in the template
    message = message_template.format(user_input=userInput, available_queries=available_queries)

    # Send the message to the model and get the response
    response = chat.send_message(message)
    return response
