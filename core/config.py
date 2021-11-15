from dotenv import load_dotenv
from passlib.context import CryptContext
import os
import string
import json

load_dotenv()

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
passwordUppercaseAlth = set(string.ascii_uppercase)
passwordDigits = set(string.digits)

skillTagsJson = json.loads(open('./skillTags.json').read())

allowdImageExtensions = set(('png', 'jpg', 'jpeg'))

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
DEV = os.getenv('TYPE') != 'PRODUCTION'
MONGO_URL = os.getenv('MONGO_URL')
ACCESS_TOKEN_EXP = os.getenv('ACCESS_TOKEN_EXP')
REFRESH_TOKEN_EXP = os.getenv('REFRESH_TOKEN_EXP')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
JWT_TOKEN_PREFIX = os.getenv('JWT_TOKEN_PREFIX')
JWT_MAX_TOKENS = os.getenv('JWT_MAX_TOKENS')
