from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Body, UploadFile
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from controllers.TokenController import getAuthorizedUser
from controllers.UserController import createUser, getUserByUsername, getUsersBySkillTags, removeUserAvatar, setUserAvatar
from core.utils import getImageFile
from db.mongodb import getDatabase
from models.UserModel import UserBaseExtended, UserInDB, UserListSuitableReq, UserRegisterReq, UserRegisterRes
from datetime import datetime
from hashlib import sha256

userRouter = APIRouter(prefix='/user', tags=['user'])

@userRouter.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserRegisterRes)
async def register(user: UserRegisterReq = Body(...), db: Database = Depends(getDatabase)):
	predictUser = getUserByUsername(db, user.username)
	if predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
	createUser(db, user)
	return getUserByUsername(db, user.username)

@userRouter.post('/list_suitable', status_code=status.HTTP_200_OK, response_model=List[UserBaseExtended])
def list_suitable(project: UserListSuitableReq = Body(...),
                  user: UserInDB = Depends(getAuthorizedUser),
                  db: Database = Depends(getDatabase)):
	project = getProjectBySlug(db, project.slug)
	if not project:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Project not found')
	projectSkillTags = list(map(lambda ob: ob['name'], project.dict()['skillTags']))
	suitableUsers = getUsersBySkillTags(db, projectSkillTags)
	return suitableUsers

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
