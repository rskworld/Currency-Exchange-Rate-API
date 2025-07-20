import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CACHE_DIR = 'cache'
    CACHE_TIME = 3600  # 1 hour in seconds
    API_KEY = os.getenv('2a7cbdc5b501224aab7f0e0d')
    BASE_URL = 'https://v6.exchangerate-api.com/v6/'