from typing import Optional
from pydantic import BaseModel, Field
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig, MyBaseModelWithExcAndInc

class MatchBase(MyBaseModelWithExcAndInc):
	username: str
	slug: str
	likeFromUser: Optional[bool] = Field(default=False)
	likeFromProject: Optional[bool] = Field(default=False)

class MatchInDB(BaseModelWithId, MatchBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'slug': 'some_cool_project',
		        'likeFromUser': 'True',
		        'LikeFromProject': 'True'
		    }
		}

# Match User Like POST (/api/match/like_user)
class MatchLikeUserReq(MatchBase):
	class Config:
		include = {'username', 'slug'}

class MatchLikeUserRes(BaseModel):
	pass

# Match Project Like POST (/api/match/like_project)
class MatchLikeProjectReq(MatchBase):
	class Config:
		include = {'slug'}

class MatchLikeProjectRes(BaseModel):
	pass
