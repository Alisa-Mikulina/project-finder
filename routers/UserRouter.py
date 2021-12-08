from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Body, UploadFile, Response
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from controllers.TokenController import getAuthorizedUser
from controllers.UserController import *
from core.config import REFRESH_TOKEN_EXP
from core.errors import API_ERRORS
from controllers.UserController import checkPasswordHash
from controllers.TokenController import generateToken
from core.utils import slugifyUniqueString
from db.mongodb import getDatabase
from models.ProjectModel import UserListSuitableReq
from models.UserModel import *

userRouter = APIRouter(prefix='/user', tags=['user'])

@userRouter.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserRegisterRes)
async def registerUserEP(user: UserRegisterReq = Body(...), db: Database = Depends(getDatabase)):
	slugUsername = slugifyUniqueString(user.username)
	predictUser = getUserByUsername(db, slugUsername)
	if predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['user.AlreadyExists'])
	createUser(db, user, slugUsername)
	return getUserByUsername(db, slugUsername)

@userRouter.post('/login', status_code=status.HTTP_200_OK, response_model=UserLoginRes)
async def loginUserEP(response: Response, user: UserLoginReq = Body(...),
                      db: Database = Depends(getDatabase)):
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
	                    expires=int(REFRESH_TOKEN_EXP) * 60**2,
	                    httponly=True)
	return {'accessToken': accessToken, 'refreshToken': refreshToken, 'expires': refreshTokenExpires}

@userRouter.post('/list_suitable', status_code=status.HTTP_200_OK, response_model=List[UserListSuitableRes])
def listSuitableEP(req: UserListSuitableReq = Body(...),
                   user: UserInDB = Depends(getAuthorizedUser),
                   db: Database = Depends(getDatabase)):
	project = getProjectBySlug(db, req.slug)
	if not project:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NotFound'])
	projectSkillTags = list(map(lambda ob: ob['label'], project.dict()['skillTags']))
	suitableUsers = getUsersBySkillTags(db, user.username, projectSkillTags, req.skip, req.limit)
	return suitableUsers

# @userRouter.post('/avatar', status_code=status.HTTP_200_OK)
# async def changeAvatar(user: UserInDB = Depends(getAuthorizedUser),
#                        avatarFile: UploadFile = Depends(getImageFile),
#                        db: Database = Depends(getDatabase)):
# 	fileExtension = avatarFile.filename.split('.')[-1]
# 	fileName = sha256(f'{int(datetime.utcnow().timestamp())}{avatarFile.filename}'.encode()).hexdigest()
# 	fileName = f'{fileName}.{fileExtension}'
# 	try:
# 		await removeUserAvatar(db, user)
# 		await setUserAvatar(db, user, avatarFile, fileName)
# 	except:
# 		await removeUserAvatar(db, user)
# 		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong')
# 	return {'avatarUrl': f'/media/avatars/{fileName}'}

@userRouter.get('/me', status_code=status.HTTP_200_OK, response_model=UserSelfRes)
async def getSelfInfoEP(user: UserInDB = Depends(getAuthorizedUser), db: Database = Depends(getDatabase)):
	return user

@userRouter.post('/me', status_code=status.HTTP_200_OK, response_model=UserSelfChangeRes)
async def chnageSelfInfoEP(userChange: UserSelfChangeReq = Body(...),
                           user: UserInDB = Depends(getAuthorizedUser),
                           db: Database = Depends(getDatabase)):
	changeUser(db, user.username, userChange)
	return getUserByUsername(db, user.username)

@userRouter.get('/{username}', status_code=status.HTTP_200_OK, response_model=UserInfoRes)
async def getUserEP(username: str,
                    user: UserInDB = Depends(getAuthorizedUser),
                    db: Database = Depends(getDatabase)):
	userProfile = getUserByUsername(db, username)
	if not userProfile:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['user.NotFound'])
	return userProfile