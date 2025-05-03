# src/priceoye/config.py
from agents import set_default_openai_api, set_default_openai_client
from openai import AsyncOpenAI  
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
set_default_openai_api('chat_completions')
Model_='gemini-2.0-flash'
llm= AsyncOpenAI(api_key=API_KEY, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
set_default_openai_client(llm)