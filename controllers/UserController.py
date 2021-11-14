from bson.objectid import ObjectId
from pymongo.database import Database
from core.config import pwdContext
import aiofiles.os
from fastapi import UploadFile

from models.UserModel import UserInDB, UserRegisterReq

def getUserByUsername(db: Database, username: str) -> UserInDB:
	user = db.users.find_one({'username': username})
	if user:
		return UserInDB(**user)

def getUserById(db: Database, user_id: str) -> UserInDB:
	user = db.users.find_one({'_id': ObjectId(user_id)})
	if user:
		return UserInDB(**user)

def createUser(db: Database, user: UserRegisterReq):
	hashedPassword = generatePasswordHash(user.password)
	newUser = UserInDB(**{**user.dict(), 'passwordHash': hashedPassword})
	db.users.insert_one(newUser.dict())

def generatePasswordHash(password: str):
	return pwdContext.hash(password)

def checkPasswordHash(password: str, passwordHash: str):
	return pwdContext.verify(password, passwordHash)

async def setUserAvatar(db: Database, user: UserInDB, avatarFile: UploadFile, fileName: str):
	async with aiofiles.open(f'./media/avatars/{fileName}', 'wb') as outFile:
		while content := await avatarFile.read(1024):
			await outFile.write(content)
	db.users.find_one_and_update({'_id': user.id}, {'$set': {'avatarUrl': f'/media/avatars/{fileName}'}})

async def removeUserAvatar(db: Database, user: UserInDB):
	if user.avatarUrl:
		db.users.find_one_and_update({'_id': user.id}, {'$set': {'avatarUrl': ''}})
		await aiofiles.os.remove(f'./{user.avatarUrl}')