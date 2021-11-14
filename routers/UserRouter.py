from fastapi import APIRouter, status, HTTPException, Depends, Body, UploadFile
from pymongo.database import Database
from controllers.TokenController import getAuthorizedUser
from controllers.UserController import createUser, getUserByUsername, removeUserAvatar, setUserAvatar
from core.utils import getImageFile
from db.mongodb import getDatabase
from models.UserModel import UserInDB, UserRegisterReq
import aiofiles
from datetime import datetime
from hashlib import sha256

userRouter = APIRouter(prefix='/user', tags=['user'])

@userRouter.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisterReq = Body(...), db: Database = Depends(getDatabase)):
	predictUser = getUserByUsername(db, user.username)
	if predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
	createUser(db, user)
	return {}

@userRouter.post('/avatar', status_code=status.HTTP_200_OK)
async def changeAvatar(user: UserInDB = Depends(getAuthorizedUser),
                       avatarFile: UploadFile = Depends(getImageFile),
                       db: Database = Depends(getDatabase)):
	fileExtension = avatarFile.filename.split('.')[-1]
	fileName = sha256(f'{int(datetime.utcnow().timestamp())}{avatarFile.filename}'.encode()).hexdigest()
	fileName = f'{fileName}.{fileExtension}'
	try:
		await removeUserAvatar(db, user)
		await setUserAvatar(db, user, avatarFile, fileName)
	except:
		await removeUserAvatar(db, user)
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong')
	return {'avatarUrl': f'/media/avatars/{fileName}'}
