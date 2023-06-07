import os
from dotenv import *

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PAYME = os.getenv('BOT_PAYMENT')
IMAGE_PATH = os.getenv('IMAGE_PATH')

DB_NAME = os.getenv('DB_NAME'),
DB_USER = os.getenv('DB_USER'),
DB_PASSWORD = os.getenv('DB_PASSWORD'),
DB_HOST = os.getenv('DB_HOST'),
DB_PORT = os.getenv('DB_PORT')
