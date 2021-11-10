from fastapi import APIRouter, status, HTTPException, Depends, Body
from pymongo.database import Database
from controllers.TokenController import generateToken
from controllers.UserController import checkPasswordHash, createUser, generatePasswordHash, getUserByUsername
from db.mongodb import getDatabase

from models.UserModel import UserLoginReq, UserRegisterReq

userRouter = APIRouter()

@userRouter.post('/register', tags=['user'], status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisterReq = Body(...), db: Database = Depends(getDatabase)):
	predictUser = getUserByUsername(db, user.username)
	if predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
	createUser(db, user)
	return {}

@userRouter.post('/login', tags=['user'], status_code=status.HTTP_200_OK)
async def login(user: UserLoginReq = Body(...), db: Database = Depends(getDatabase)):
	userInDB = getUserByUsername(db, user.username)
	if not userInDB or not checkPasswordHash(user.password, userInDB.password_hash):
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid username or password')
	token = generateToken(db, userInDB)
	return {'token': token}
