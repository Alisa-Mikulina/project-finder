from typing import Optional
from pydantic import Field, BaseModel
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.UserModel import UserUsername

class RefreshTokenBase(UserUsername):
	refreshToken: str = Field(...)
	expires: int = Field(...)
	fingerPrint: str = Field(...)

# RefreshToken Refresh POST (/api/auth/refresh_token)
class RefreshTokenRefreshReq(RefreshTokenBase):
	refreshToken: Optional[str] = Field(default='')

	class Config:
		include = {'fingerPrint'}

class RefreshTokenRefreshRes(BaseModel):
	accessToken: str = Field(...)
	refreshToken: str = Field(...)

class RefreshTokenInDB(RefreshTokenBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'refreshToken': 'my refresh token',
		        'fingerPrint': 'my unique finger print',
		        'expires': 123456789
		    }
		}
