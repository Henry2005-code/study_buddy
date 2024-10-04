import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit to 16 MB
