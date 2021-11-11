from pymongo.database import Database
from core.config import ACCESS_TOKEN_EXP, ACCESS_TOKEN_SECRET, JWT_MAX_TOKENS, REFRESH_TOKEN_EXP
from models.TokenModel import RefreshTokenInDB
from models.UserModel import UserInDB
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header, HTTPException, status
from db.mongodb import getDatabase
from core.config import JWT_TOKEN_PREFIX
from controllers.UserController import getUserByUsername
from uuid import uuid4

def generateToken(db: Database, user: UserInDB, fingerPrint: str) -> str:
	payload = {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXP))}
	accessToken = jwt.encode(payload, ACCESS_TOKEN_SECRET, 'HS256')
	refreshTokenExpires = datetime.utcnow() + timedelta(hours=int(REFRESH_TOKEN_EXP))
	refreshTokenInDB = RefreshTokenInDB(
	    **{
	        'user_id': str(user.id),
	        'refreshToken': uuid4().hex,
	        'expires': int(refreshTokenExpires.timestamp()),
	        'fingerPrint': fingerPrint
	    })

	db.refreshTokens.delete_one({'fingerPrint': fingerPrint})
	userTokens = list(db.refreshTokens.find({'user_id': str(user.id)}))
	if len(userTokens) >= int(JWT_MAX_TOKENS):
		db.refreshTokens.delete_many({'user_id': str(user.id)})
	db.refreshTokens.insert_one(refreshTokenInDB.dict())
	return [accessToken, refreshTokenInDB.refreshToken, refreshTokenExpires]

def getRefreshTokenByUUID(refreshToken: str, db: Database = Depends(getDatabase)):
	refreshTokenInDB = db.refreshTokens.find_one({'refreshToken': refreshToken})
	if refreshTokenInDB:
		return RefreshTokenInDB(**refreshTokenInDB)

def deleteRefreshTokenByUUID(refreshToken: str, db: Database = Depends(getDatabase)):
	db.refreshTokens.delete_one({'refreshToken': refreshToken})

def getAuthorizedUser(db: Database = Depends(getDatabase), authorization: str = Header(...)):
	credentialsException = HTTPException(
	    status_code=status.HTTP_401_UNAUTHORIZED,
	    detail="Could not validate credentials",
	    headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		tokenPrefix, accessToken = authorization.split(" ")
		if tokenPrefix != JWT_TOKEN_PREFIX:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization type')
	except:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization type')
	try:
		payload = jwt.decode(accessToken, ACCESS_TOKEN_SECRET, 'HS256')
		username = payload['username']
	except JWTError:
		raise credentialsException
	user = getUserByUsername(db, username)
	if not user:
		raise credentialsException
	return user
