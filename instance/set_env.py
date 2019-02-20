import os
from os.path import join, dirname
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# create .env file path
dotenv_path = join(BASE_DIR, '.env')

# load .env from the path
load_dotenv(dotenv_path)
