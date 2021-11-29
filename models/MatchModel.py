from typing import List, Optional
from fastapi.datastructures import Default
from pydantic import BaseModel, Field, validator
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.UserModel import UserBaseExtended, UserInDB
from models.ProjectModel import ProjectBaseWithoutUser, ProjectInDB

class MatchBase(BaseModel):
	username: str
	slug: str
	likeFromUser: Optional[bool] = ()
	likeFromProject: Optional[bool] = ()

class MatchCreateReq(BaseModel):
	username: str
	slug: str

class MatchInDB(BaseModelWithId, MatchBase):
	username: str
	slug: str

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'slug': 'some_cool_project',
		        'likeFromUser': 'True',
		        'LikeFromProject': 'True'
		    }
		}
