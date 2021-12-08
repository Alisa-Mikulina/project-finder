from typing import Optional
from pydantic import BaseModel, Field
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig, MyBaseModelWithExcAndInc

class MatchBase(MyBaseModelWithExcAndInc):
	username: str
	slug: str
	projectTitle: str = Field(min_length=3, max_length=35)
	likeFromUser: bool = Field(default=False)
	likeFromProject: bool = Field(default=False)

class MatchInDB(BaseModelWithId, MatchBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'slug': 'some_cool_project',
		        'projectTitle': 'Some cool project',
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

# Get self mathces GET (/api/match/my_matches)

class MatchGetSelfReq(BaseModel):
	pass

class MatchGetSelfRes(MatchBase):
	class Config:
		include = {'username', 'slug', 'projectTitle'}

# Get self project mathces POST (/api/match/my_project_matches)

class MatchGetSelfProjectReq(MatchBase):
	class Config:
		include = {'slug'}

class MatchGetSelfProjectRes(MatchBase):
	class Config:
		include = {'username', 'slug', 'projectTitle'}
