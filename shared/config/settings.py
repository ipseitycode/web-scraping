import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", 8000))

API_KEY = os.getenv("API_KEY")