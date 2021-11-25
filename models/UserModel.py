from typing import List, Optional
from pydantic import BaseModel, Field, validator
from core.config import passwordUppercaseAlth, passwordDigits
from core.utils import slugifyString
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.SkillTagModel import SkillTagBase

class UserBase(BaseModel):
	username: str = Field(min_length=8, max_length=50)

	@validator('username')
	def checkUsername(cls, username):
		if username != slugifyString(username, False):
			raise ValueError('Wrong username format')
		return username

class UserBaseExtended(UserBase):
	name: str = Field(min_length=1, max_length=50)
	lastname: str = Field(min_length=1, max_length=50)
	contact: str = Field(min_length=3, max_length=50)
	information: str = Field(min_length=20, max_length=500)
	skillTags: Optional[List[SkillTagBase]] = []

class UserPasswordWithValidator(BaseModel):
	password: str = Field(min_length=8, max_length=50)

	@validator('password')
	def checkPassword(cls, password):
		if not any([char in passwordUppercaseAlth for char in password]):
			raise ValueError('Password must contain uppercase characters')
		if not any([char in passwordDigits for char in password]):
			raise ValueError('Password must contain digits')
		return password

class UserLoginReq(UserBase, UserPasswordWithValidator):
	fingerPrint: str = Field(...)

class UserLoginRes(BaseModel):
	token: str = Field(...)

class UserRegisterReq(UserBaseExtended, UserPasswordWithValidator):
	pass

class UserChangeReq(BaseModel):
	name: str = Field(min_length=1, max_length=50)
	lastname: str = Field(min_length=1, max_length=50)
	contact: str = Field(min_length=3, max_length=50)
	information: str = Field(min_length=20, max_length=500)
	skillTags: Optional[List[SkillTagBase]] = []

class UserRegisterRes(UserBaseExtended):
	coverUrl: str = Field(default='')

class UserListSuitableReq(BaseModel):
	slug: str = Field(min_length=3, max_length=35)

class UserInDB(BaseModelWithId, UserBaseExtended):
	coverUrl: str = Field(default='')
	passwordHash: str = Field(default='')

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'name': 'MyName',
		        'lastname': 'MyLastname',
		        'contact': 'MyContact',
		        'passwordHash': 'adhahduad123u1',
		        'coverUrl': '/media/avatars/akdlakldklakl.jpeg'
		    }
		}
