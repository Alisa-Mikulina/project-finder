from typing import Optional
from fastapi import APIRouter, status, HTTPException, Depends, Body, Response, Cookie
from pymongo.database import Database
from controllers.TokenController import deleteRefreshTokenByUUID, generateToken, getRefreshTokenByUUID
from controllers.UserController import checkPasswordHash, getUserById, getUserByUsername
from core.errors import API_ERRORS
from db.mongodb import getDatabase
from models.TokenModel import RefreshTokenReq
from datetime import datetime, timedelta

from models.UserModel import UserLoginReq

authRouter = APIRouter(prefix='/auth', tags=['auth'])

@authRouter.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response, user: UserLoginReq = Body(...), db: Database = Depends(getDatabase)):
	userInDB = getUserByUsername(db, user.username)
	if not userInDB:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['username.InvalidUsername'])
	if not checkPasswordHash(user.password, userInDB.passwordHash):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['password.InvalidPassword'])
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
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['auth.MissingRefreshToken'])

	exactRefreshToken = token.refreshToken if token.refreshToken else refreshToken
	refreshTokenInDB = getRefreshTokenByUUID(refreshToken=exactRefreshToken, db=db)

	if not refreshTokenInDB:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['auth.InvalidToken'])

	deleteRefreshTokenByUUID(refreshToken=exactRefreshToken, db=db)

	if token.fingerPrint != refreshTokenInDB.fingerPrint:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['auth.InvalidFingerPrint'])

	if datetime.fromtimestamp(refreshTokenInDB.expires) - datetime.utcnow() <= timedelta():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['auth.RefreshTokenExpired'])

	userInDB = getUserById(db=db, userId=refreshTokenInDB.userId)
	accessToken, refreshToken, refreshTokenExpires = generateToken(db, userInDB, token.fingerPrint)
	response.set_cookie(key='refreshToken',
	                    value=refreshToken,
	                    expires=refreshTokenExpires,
	                    httponly=True,
	                    path='/api/auth')
	return {'accessToken': accessToken, 'refreshToken': refreshToken}
