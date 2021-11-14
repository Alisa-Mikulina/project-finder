from typing import Optional
from pydantic import BaseModel, Field, validator
from core.config import passwordUppercaseAlth, passwordDigits
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig

class UserBase(BaseModel):
	username: str = Field(min_length=8, max_length=50)

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

class UserRegisterReq(UserBase, UserPasswordWithValidator):
	name: str = Field(min_length=1, max_length=50)
	lastname: str = Field(min_length=1, max_length=50)
	contact: str = Field(min_length=3, max_length=50)
	information: str = Field(min_length=20, max_length=500)

class UserInDB(BaseModelWithId, UserBase):
	name: str = Field(default='')
	lastname: str = Field(default='')
	contact: str = Field(default='')
	information: str = Field(default='')
	passwordHash: str = Field(default='')
	avatarUrl: str = Field(default='')

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    "example": {
		        "username": "My goodName",
		        "name": "MyName",
		        "lastname": "MyLastname",
		        "contact": "MyContact",
		        "passwordHash": "adhahduad123u1"
		    }
		}
