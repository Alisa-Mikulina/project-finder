from typing import Optional
from fastapi import APIRouter, status, HTTPException, Depends, Body, Response, Cookie
from pymongo.database import Database
from controllers.TokenController import deleteRefreshTokenByUUID, generateToken, getRefreshTokenByUUID
from controllers.UserController import checkPasswordHash, createUser, getUserById, getUserByUsername
from db.mongodb import getDatabase
from models.TokenModel import RefreshTokenInDB, RefreshTokenReq
from datetime import datetime, timedelta

from models.UserModel import UserLoginReq, UserRegisterReq

authRouter = APIRouter(prefix='/auth', tags=['auth'])

@authRouter.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response, user: UserLoginReq = Body(...), db: Database = Depends(getDatabase)):
	userInDB = getUserByUsername(db, user.username)
	if not userInDB or not checkPasswordHash(user.password, userInDB.password_hash):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid username or password')
	accessToken, refreshToken, refreshTokenExpires = generateToken(db, userInDB, user.fingerPrint)

	#TODO - Проверить параметры на безопасность после поднятия на сервере
	response.set_cookie(key='refreshToken',
	                    value=refreshToken,
	                    expires=refreshTokenExpires,
	                    httponly=True,
	                    path='/api/auth')
	return {'accessToken': accessToken, 'refreshToken': refreshToken}

@authRouter.post('/refresh_token', status_code=status.HTTP_200_OK)
async def refreshToken(response: Response,
                       token: RefreshTokenReq = Body(...),
                       refreshToken: Optional[str] = Cookie(None),
                       db: Database = Depends(getDatabase)):
	if not token.refreshToken and not refreshToken:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing refresh token')

	exactRefreshToken = token.refreshToken if token.refreshToken else refreshToken
	refreshTokenInDB = getRefreshTokenByUUID(refreshToken=exactRefreshToken, db=db)

	if not refreshTokenInDB:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')

	deleteRefreshTokenByUUID(refreshToken=exactRefreshToken, db=db)

	if token.fingerPrint != refreshTokenInDB.fingerPrint:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid fingerPrint')

	if datetime.fromtimestamp(refreshTokenInDB.expires) - datetime.utcnow() <= timedelta():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Refresh token expired')

	userInDB = getUserById(db=db, user_id=refreshTokenInDB.user_id)
	accessToken, refreshToken, refreshTokenExpires = generateToken(db, userInDB, token.fingerPrint)
	response.set_cookie(key='refreshToken',
	                    value=refreshToken,
	                    expires=refreshTokenExpires,
	                    httponly=True,
	                    path='/api/auth')
	return {'accessToken': accessToken, 'refreshToken': refreshToken}
