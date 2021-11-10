from pymongo.database import Database
from core.config import ACCESS_TOKEN_EXP, ACCESS_TOKEN_SECRET
from models.UserModel import UserInDB
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header, HTTPException, status
from db.mongodb import getDatabase
from core.config import JWT_TOKEN_PREFIX
from controllers.UserController import getUserByUsername

def generateToken(db: Database, user: UserInDB) -> str:
	payload = {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXP))}
	encodedJwt = jwt.encode(payload, ACCESS_TOKEN_SECRET, 'HS256')
	return encodedJwt

def getAuthorizedUser(db: Database = Depends(getDatabase), authorization: str = Header(...)):
	credentialsException = HTTPException(
	    status_code=status.HTTP_401_UNAUTHORIZED,
	    detail="Could not validate credentials",
	    headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		tokenPrefix, token = authorization.split(" ")
		if tokenPrefix != JWT_TOKEN_PREFIX:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization type')
	except:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization type')

	try:
		payload = jwt.decode(token, ACCESS_TOKEN_SECRET, 'HS256')
		username = payload['username']
	except JWTError:
		raise credentialsException
	user = getUserByUsername(db, username)
	if not user:
		raise credentialsException
	return user
