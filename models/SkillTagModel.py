from pydantic import BaseModel, Field, validator
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from core.config import skillTagsJson

class SkillTagBase(BaseModel):
	name: str = Field(min_length=3, max_length=20)

	@validator('name')
	def checkName(cls, name):
		if name not in skillTagsJson.keys():
			raise ValueError('Skill name is not allowed')
		return name

class SkillTagInDB(BaseModelWithId, SkillTagBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {"example": {"name": "ReacJS"}}
