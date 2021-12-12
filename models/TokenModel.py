from typing import Optional
from pydantic import Field
from models.UserModel import UserUsername
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig, MyBaseModelWithExcAndInc, RegisterModelExcInc

class RefreshTokenBase(UserUsername):
	refreshToken: str = Field(...)
	expires: int = Field(...)
	fingerPrint: str = Field(...)

# RefreshToken Refresh POST (/api/auth/refresh_token)
class RefreshTokenRefreshReq(RefreshTokenBase):
	refreshToken: str = Field(default='')

	class Config:
		include = {'fingerPrint', 'refreshToken'}

RegisterModelExcInc(RefreshTokenRefreshReq)

class RefreshTokenRefreshRes(MyBaseModelWithExcAndInc):
	accessToken: str = Field(...)
	refreshToken: str = Field(...)
	expires: int = Field(...)

class RefreshTokenInDB(BaseModelWithId, RefreshTokenBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'refreshToken': 'my refresh token',
		        'fingerPrint': 'my unique finger print',
		        'expires': 123456789
		    }
		}
