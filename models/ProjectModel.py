from typing import Optional
from pydantic import Field
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from models.SkillTagModel import SkillTagListRequired
from models.UserModel import UserBase

class ProjectBase(SkillTagListRequired):
	title: str = Field(min_length=3, max_length=35)
	description: Optional[str] = Field(default='', max_length=500)
	slug: str = Field(min_length=3, max_length=35)
	user: UserBase
	avatarUrl: Optional[str] = Field(default='')
	coverUrl: Optional[str] = Field(default='')

class ProjectInDB(BaseModelWithId, ProjectBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {
		    'example': {
		        'title': 'Our cool project',
		        'description': 'Really cool description of really cool project',
		        'skillTags': [{
		            'label': 'ReactJS'
		        }],
		        'slug': 'our_cool_project',
		        'user': {
		            'username': 'My goodName',
		            'name': 'MyName',
		            'lastname': 'MyLastname',
		            'contact': {
		                'email': 'MyEmail',
		                'telegram': 'MyTelegram',
		                'website': 'MyWebsite'
		            },
		            'gender': 0,
		            'birthDate': '13.12.1337',
		            'location': 'MyLocation',
		            'information': 'MyInformation',
		            'skillTags': [{
		                'label': 'ReactJS'
		            }],
		            'avatarUrl': '/media/avatars/adwada.jpg',
		            'coverUrl': '/media/avatars/akdlakldklakl.jpeg'
		        },
		        'avatarUrl': '/media/avatars/adwad.jpg',
		        'coverUrl': '/media/avatars/adwadaw.jpg'
		    }
		}

# Project Create POST (/api/project/create)
class ProjectCreateReq(ProjectBase):
	class Config:
		include = {'title', 'description', 'skillTags'}

class ProjectChangeRes(ProjectBase):
	pass

# Project My GET (/api/project/my)

class ProjectMyRes(ProjectBase):
	pass

# Project My POST (/api/project/my)

class ProjectChangeMyReq(ProjectBase):
	class Config:
		include = {'description', 'skillTags'}

class ProjectChangeMyRes(ProjectBase):
	pass

# Project Info GET (/api/project/<slug>)

class ProjectInfoRes(ProjectBase):
	pass