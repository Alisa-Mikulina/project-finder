from typing import List
from pydantic import BaseModel, Field
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.SkillTagModel import SkillTagBase
from models.UserModel import UserBaseExtended, UserInDB

class ProjectBase(BaseModel):
	title: str = Field(min_length=3, max_length=35)
	description: str = Field(min_length=20, max_length=500)
	skillTags: List[SkillTagBase] = Field(min_items=1)
	slug: str = Field(min_length=3, max_length=35)
	user: UserBaseExtended
	coverUrl: str = Field(default='')

class ProjectBaseWithoutUser(BaseModel):
	title: str = Field(min_length=3, max_length=35)
	description: str = Field(min_length=20, max_length=500)
	skillTags: List[SkillTagBase] = Field(min_items=1)
	slug: str = Field(min_length=3, max_length=35)
	coverUrl: str = Field(default='')

class ProjectCreateReq(BaseModel):
	title: str = Field(min_length=3, max_length=35)
	description: str = Field(min_length=20, max_length=500)
	skillTags: List[SkillTagBase] = Field(min_items=1)

class ProjectChangeReq(BaseModel):
	description: str = Field(min_length=20, max_length=500)
	skillTags: List[SkillTagBase] = Field(min_items=1)

class ProjectInDB(BaseModelWithId, ProjectBase):
	user: UserInDB

	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'title': 'Our cool project',
		        'description': 'Really cool description of really cool project',
		        'skillTags': [{
		            'label': 'ReactJS'
		        }],
		        'slug': 'our_cool_project',
		        'userId': 'ajkdjadjiadi2i13nankd',
		        'coverUrl': '/media/avatars/adwadaw.jpg'
		    }
		}
