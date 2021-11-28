from typing import Optional
from pydantic import BaseModel, Field, validator
from core.config import passwordUppercaseAlth, passwordDigits
from core.utils import slugifyString
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.SkillTagModel import SkillTagList

class UserUsername(BaseModel):
	username: str = Field(min_length=8, max_length=50)

	@validator('username')
	def checkUsername(cls, username):
		if username != slugifyString(username, False):
			raise ValueError('Wrong username format')
		return username

class UserPassword(BaseModel):
	password: str = Field(min_length=8, max_length=50)

	@validator('password')
	def checkPassword(cls, password):
		if not any([char in passwordUppercaseAlth for char in password]):
			raise ValueError('Password must contain uppercase characters')
		if not any([char in passwordDigits for char in password]):
			raise ValueError('Password must contain digits')
		return password

class UserContacts(BaseModel):
	email: Optional[str] = Field(default='', max_length=50)
	telegram: Optional[str] = Field(default='', max_length=50)
	website: Optional[str] = Field(default='', max_length=50)

class UserBase(UserUsername, SkillTagList):
	name: str = Field(min_length=2, max_length=50)
	lastname: str = Field(min_length=2, max_length=50)
	contact: Optional[UserContacts] = Field(default=UserContacts())
	gender: Optional[bool] = Field(default=False)
	birthDate: Optional[str] = Field(default='')
	location: Optional[str] = Field(default='')
	information: Optional[str] = Field(default='', max_length=1200)
	avatarUrl: Optional[str] = Field(default='')
	coverUrl: Optional[str] = Field(default='')

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

class UserLoginRes(BaseModel):
	accessToken: str = Field(...)
	refreshToken: str = Field(...)

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

# User List Suitable
class UserListSuitableReq(BaseModel):
	slug: str = Field(min_length=3, max_length=35)
