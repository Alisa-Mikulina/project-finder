from typing import List, Optional
from pydantic import BaseModel, Field, validator
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.UserModel import UserBaseExtended, UserInDB
from models.ProjectModel import ProjectBaseWithoutUser, ProjectInDB

class MatchBase(BaseModel):
	username: UserBaseExtended.username
	slug: ProjectBaseWithoutUser.slug
	likeFromUser: Optional[bool] = ()
	likeFromProject: Optional[bool] = ()

class MatchCreateReq(BaseModel):
	username: UserBaseExtended.username
	slug: ProjectBaseWithoutUser.slug

class MatchInDB(BaseModelWithId, MatchBase):
	username: UserInDB.username
	slug: ProjectInDB.slug

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'username': 'My goodName',
		        'slug': 'some_cool_project',
		        'likeFromUser': 'True',
		        'LikeFromProject': 'True'
		    }
		}
