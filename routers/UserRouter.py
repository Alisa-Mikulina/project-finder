from fastapi import APIRouter, status, HTTPException, Depends, Body, Response
from pymongo.database import Database
from controllers.TokenController import generateToken
from controllers.UserController import checkPasswordHash, createUser, getUserByUsername
from db.mongodb import getDatabase

from models.UserModel import UserLoginReq, UserRegisterReq

userRouter = APIRouter(prefix='/user', tags=['user'])

@userRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisterReq = Body(...), db: Database = Depends(getDatabase)):
	predictUser = getUserByUsername(db, user.username)
	if predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
	createUser(db, user)
	return {}
