from pymongo.database import Database
from core.config import ACCESS_TOKEN_EXP, ACCESS_TOKEN_SECRET, JWT_MAX_TOKENS, REFRESH_TOKEN_EXP
from core.errors import API_ERRORS
from models.TokenModel import RefreshTokenInDB
from models.UserModel import UserInDB
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Security
from db.mongodb import getDatabase
from core.config import JWT_TOKEN_PREFIX, bearerSecurity
from controllers.UserController import getUserByUsername
from uuid import uuid4
from fastapi.security import HTTPAuthorizationCredentials

def generateToken(db: Database, user: UserInDB, fingerPrint: str):
	payload = {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXP))}
	accessToken = jwt.encode(payload, ACCESS_TOKEN_SECRET, 'HS256')
	refreshTokenExpires = datetime.utcnow() + timedelta(hours=int(REFRESH_TOKEN_EXP))
	refreshTokenInDB = RefreshTokenInDB(
	    **{
	        'username': str(user.username),
	        'refreshToken': uuid4().hex,
	        'expires': int(refreshTokenExpires.timestamp()),
	        'fingerPrint': fingerPrint
	    })

	db.refreshTokens.delete_one({'fingerPrint': fingerPrint})
	userTokens = list(db.refreshTokens.find({'userId': str(user.id)}))
	if len(userTokens) >= int(JWT_MAX_TOKENS):
		db.refreshTokens.delete_many({'userId': str(user.id)})
	db.refreshTokens.insert_one(refreshTokenInDB.dict())
	return [accessToken, refreshTokenInDB.refreshToken, refreshTokenExpires]

def getRefreshTokenByValue(refreshToken: str, db: Database = Depends(getDatabase)):
	refreshTokenInDB = db.refreshTokens.find_one({'refreshToken': refreshToken})
	if refreshTokenInDB:
		return RefreshTokenInDB(**refreshTokenInDB)

def deleteRefreshTokenByValue(refreshToken: str, db: Database = Depends(getDatabase)):
	db.refreshTokens.delete_one({'refreshToken': refreshToken})

async def getAuthorizedUser(
    authorization: HTTPAuthorizationCredentials = Security(bearerSecurity),
    db: Database = Depends(getDatabase),
):
	credentialsException = HTTPException(
	    status_code=status.HTTP_401_UNAUTHORIZED,
	    detail=API_ERRORS['auth.CredentialsValidationError'],
	    headers={'WWW-Authenticate': 'Bearer'},
	)
	try:
		tokenPrefix = authorization.scheme
		accessToken = authorization.credentials
		if tokenPrefix != JWT_TOKEN_PREFIX:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
			                    detail=API_ERRORS['auth.AuthorizationTypeError'])
	except:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
		                    detail=API_ERRORS['auth.AuthorizationTypeError'])
	try:
		payload = jwt.decode(accessToken, ACCESS_TOKEN_SECRET, 'HS256')
		username = payload['username']
	except JWTError:
		raise credentialsException
	user = getUserByUsername(db, username)
	if not user:
		raise credentialsException
	return user
