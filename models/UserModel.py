from typing import Optional
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig

class UserBase(BaseModel):
	username: str = Field(min_length=8, max_length=50)

class UserLoginReq(BaseModel):
	username: str = Field(min_length=8, max_length=50)
	password: str = Field(min_length=8, max_length=50)
	fingerPrint: str = Field(...)

class UserLoginRes(BaseModel):
	token: str = Field(...)

class UserRegisterReq(UserBase):
	password: str = Field(min_length=8, max_length=50)
	name: str = Field(min_length=1, max_length=50)
	lastname: str = Field(min_length=1, max_length=50)
	contact: str = Field(min_length=3,max_length=50)
	information: str = Field(min_length=20,max_length=500)

class UserInDB(BaseModelWithId, UserBase):
	name: str = Field(default='')
	lastname: str = Field(default='')
	contact: str = Field(default='')
	information: str = Field(default='')
	password_hash: str = Field(default='')

	class Config(BaseModelWithIdConfig):
		schema_extra = {"example": {"username": "My goodName", "name": "MyName", "lastname": "MyLastname", "contact": "MyContact", "password_hash": "adhahduad123u1"}}
