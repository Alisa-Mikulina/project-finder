from typing import Optional
from dotenv import load_dotenv
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette.requests import Request
import os
import string
import json

from fastapi.security import HTTPBearer
from starlette import status

from core.errors import API_ERRORS

load_dotenv()

pwdContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

skillTagsJson = json.loads(open('./skillTags.json').read())

allowedImageExtensions = set(('png', 'jpg', 'jpeg'))

uniqueSlugifyRegexp = r'[^-a-zA-Z0-9_]+'
passwordValidationRegexp = r'^[a-zA-Z0-9!"#$%&\'()*+,-.\/:;<=>?@[\\\]\^_`{\|}~]+$'

class MyHTTPBearer(HTTPBearer):
	def __init__(self):
		super().__init__()

	async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
		try:
			return await super().__call__(request)
		except HTTPException as error:
			if error.detail == 'Not authenticated':
				raise HTTPException(status_code=error.status_code, detail=API_ERRORS['auth.NotAuthenticated'])
			if error.detail == 'Invalid authentication credentials':
				raise HTTPException(status_code=error.status_code, detail=API_ERRORS['auth.AuthorizationTypeError'])
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
			                    detail={
			                        'errorCode': -1,
			                        'msg': error.detail
			                    })

bearerSecurity = MyHTTPBearer()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
DEV = os.getenv('TYPE') != 'PRODUCTION'
MONGO_URL = os.getenv('MONGO_URL')
ACCESS_TOKEN_EXP = os.getenv('ACCESS_TOKEN_EXP')
REFRESH_TOKEN_EXP = os.getenv('REFRESH_TOKEN_EXP')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
JWT_TOKEN_PREFIX = os.getenv('JWT_TOKEN_PREFIX')
JWT_MAX_TOKENS = os.getenv('JWT_MAX_TOKENS')
