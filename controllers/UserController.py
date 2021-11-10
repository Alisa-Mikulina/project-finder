from pymongo.database import Database
from core.config import pwdContext

from models.UserModel import UserInDB, UserRegisterReq

def getUserByUsername(db: Database, username: str) -> UserInDB:
	user = db.users.find_one({'username': username})
	if user:
		return UserInDB(**user)

def createUser(db: Database, user: UserRegisterReq):
	hasedPassword = generatePasswordHash(user.password)
	newUser = UserInDB(**{**user.dict(), 'password_hash': hasedPassword})
	db.users.insert_one(newUser.dict())

def generatePasswordHash(password: str):
	return pwdContext.hash(password)

def checkPasswordHash(password: str, passwordHash: str):
	return pwdContext.verify(password, passwordHash)
