import re
from fastapi.exceptions import HTTPException
from pydantic import Field, validator
from starlette import status
from core.config import passwordValidationRegexp
from core.errors import API_ERRORS
from core.utils import slugifyUniqueString
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig, MyBaseModelWithExcAndInc
from models.SkillTagModel import SkillTagList

class UserUsername(MyBaseModelWithExcAndInc):
	username: str = Field(max_length=50)

	@validator('username')
	def checkUsername(cls, username):
		if len(slugifyUniqueString(username)) < 8:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['username.ToShort'])
		return username

class UserPassword(MyBaseModelWithExcAndInc):
	password: str = Field(max_length=50)

	@validator('password')
	def checkPassword(cls, password):
		if len(password) < 8:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['password.WrongLength'])
		if not re.match(passwordValidationRegexp, password):
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['password.WrongFormat'])
		return password

class UserContacts(MyBaseModelWithExcAndInc):
	email: str = Field(default='', max_length=50)
	telegram: str = Field(default='', max_length=50)
	website: str = Field(default='', max_length=50)

class UserBase(UserUsername, SkillTagList):
	name: str = Field(min_length=2, max_length=50)
	lastname: str = Field(min_length=2, max_length=50)
	contact: UserContacts = Field(default=UserContacts())
	gender: bool = Field(default=False)
	birthDate: str = Field(default='')
	location: str = Field(default='')
	information: str = Field(default='', max_length=1200)
	avatarUrl: str = Field(default='')
	coverUrl: str = Field(default='')

class UserInDB(BaseModelWithId, UserBase):
	passwordHash: str = Field(default='')

	class Config(BaseModelWithIdConfig):
		exclude = {'password'}

		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'name': 'MyName',
		        'lastname': 'MyLastname',
		        'contact': {
		            'email': 'MyEmail',
		            'telegram': 'MyTelegram',
		            'website': 'MyWebsite'
		        },
		        'gender': 0,
		        'birthDate': '13.12.1337',
		        'passwordHash': 'adhahduad123u1',
		        'location': 'MyLocation',
		        'information': 'MyInformation',
		        'skillTags': [{
		            'label': 'ReactJS'
		        }],
		        'avatarUrl': '/media/avatars/adwada.jpg',
		        'coverUrl': '/media/avatars/akdlakldklakl.jpeg'
		    }
		}

# User Login POST (/api/user/login)
class UserLoginReq(UserUsername, UserPassword):
	fingerPrint: str = Field(...)

class UserLoginRes(MyBaseModelWithExcAndInc):
	accessToken: str = Field(...)
	refreshToken: str = Field(...)
	expires: int = Field(...)

# User Register POST (/api/user/register)
class UserRegisterReq(UserBase, UserPassword):
	pass

class UserRegisterRes(UserBase):
	pass

# User Me GET (/api/user/me)

class UserSelfRes(UserBase):
	pass

# User Me POST (/api/user/me)

class UserSelfChangeReq(UserBase):
	class Config:
		exclude = {'username', 'avatarUrl', 'coverUrl'}

class UserSelfChangeRes(UserBase):
	pass

# User Info GET (/api/user/<username>)

class UserInfoRes(UserBase):
	pass

# User List Suitable POST (/api/user/list_suitable)
class UserListSuitableRes(UserBase):
	pass