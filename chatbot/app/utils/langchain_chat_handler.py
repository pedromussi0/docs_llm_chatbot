from langchain_url_handler import *
from link_scraper import *
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')