from typing import Optional
from fastapi import APIRouter, status, HTTPException, Depends, Body, Response, Cookie
from pymongo.database import Database
from controllers.TokenController import deleteRefreshTokenByValue, generateToken, getRefreshTokenByValue
from controllers.UserController import getUserByUsername
from core.errors import API_ERRORS
from db.mongodb import getDatabase
from models.TokenModel import *
from datetime import datetime, timedelta

authRouter = APIRouter(prefix='/auth', tags=['auth'])

@authRouter.post('/refresh_token', status_code=status.HTTP_200_OK, response_model=RefreshTokenRefreshRes)
async def refreshTokenEP(response: Response,
                         token: RefreshTokenRefreshReq = Body(...),
                         refreshToken: Optional[str] = Cookie(None),
                         db: Database = Depends(getDatabase)):
	if not token.refreshToken and not refreshToken:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['auth.MissingRefreshToken'])

	exactRefreshToken = token.refreshToken if token.refreshToken else refreshToken
	refreshTokenInDB = getRefreshTokenByValue(refreshToken=exactRefreshToken, db=db)

	if not refreshTokenInDB:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['auth.InvalidToken'])

	deleteRefreshTokenByValue(refreshToken=exactRefreshToken, db=db)

	if token.fingerPrint != refreshTokenInDB.fingerPrint:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['auth.InvalidFingerPrint'])

	if datetime.fromtimestamp(refreshTokenInDB.expires) - datetime.utcnow() <= timedelta():
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail=API_ERRORS['auth.RefreshTokenExpired'])

	userInDB = getUserByUsername(db=db, userId=refreshTokenInDB.username)
	accessToken, refreshToken, refreshTokenExpires = generateToken(db, userInDB, token.fingerPrint)
	response.set_cookie(key='refreshToken',
	                    value=refreshToken,
	                    expires=refreshTokenExpires,
	                    httponly=True,
	                    path='/api/auth')
	return {'accessToken': accessToken, 'refreshToken': refreshToken}
