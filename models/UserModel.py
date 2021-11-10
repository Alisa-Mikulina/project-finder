from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig

class UserBase(BaseModel):
	username: str = Field(...)
	email: EmailStr = Field(...)

class UserLoginReq(BaseModel):
	username: str = Field(...)
	password: str = Field(...)

class UserLoginRes(BaseModel):
	token: str = Field(...)

class UserRegisterReq(UserBase):
	password: str = Field(...)

class UserInDB(UserBase, BaseModelWithId):
	password_hash: str = Field(default='')

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    "example": {
		        "username": "My goodName",
		        "email": "user@example.com",
		        "password_hash": "adhahduad123u1"
		    }
		}
