from dotenv import load_dotenv
from passlib.context import CryptContext
import os

load_dotenv()

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
DEV = os.getenv('TYPE') != 'PRODUCTION'
MONGO_URL = os.getenv('MONGO_URL')
ACCESS_TOKEN_EXP = os.getenv('ACCESS_TOKEN_EXP')
REFRESH_TOKEN_EXP = os.getenv('REFRESH_TOKEN_EXP')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
JWT_TOKEN_PREFIX = os.getenv('JWT_TOKEN_PREFIX')
JWT_MAX_TOKENS = os.getenv('JWT_MAX_TOKENS')
