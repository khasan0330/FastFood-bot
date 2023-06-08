import os
from dotenv import *

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
PAYME = os.getenv('BOT_PAYMENT')
IMAGE_PATH = os.getenv('IMAGE_PATH')

DB_NAME = os.getenv('POSTGRES_DB'),
DB_USER = os.getenv('POSTGRES_USER'),
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD'),
DB_HOST = os.getenv('POSTGRES_ADDR'),
DB_PORT = os.getenv('POSTGRES_PORT')
