import os
import base64
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

SERVER_HOST = os.getenv('SERVER_HOST')
CHAIN_HOST = os.getenv('REACT_APP_CHAIN_HOST')
APP_PK = base64.b16decode(os.getenv('REACT_APP_APP_PK'))
APP_SK = base64.b16decode(os.getenv('REACT_APP_APP_SK'))
APP_ADDR = os.getenv('REACT_APP_APP_ID')