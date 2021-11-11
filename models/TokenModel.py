from typing import Optional
from pydantic import Field, BaseModel
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig

class RefreshTokenReq(BaseModel):
	fingerPrint: str = Field(...)
	refreshToken: Optional[str]

class RefreshTokenInDB(BaseModelWithId):
	user_id: str = Field(...)
	refreshToken: str = Field(...)
	expires: int = Field(...)
	fingerPrint: str = Field(...)

	class Config(BaseModelWithIdConfig):
		schema_extra = {"example": {"username": "My goodName", "password_hash": "adhahduad123u1"}}
