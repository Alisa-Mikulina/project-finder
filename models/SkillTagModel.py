from pydantic import BaseModel, Field, validator
from models.BaseModel import BaseModelWithId, BaseModelWithIdConfig
from core.config import skillTagsJson

class SkillTagBase(BaseModel):
	label: str = Field(min_length=3, max_length=20)

	@validator('label')
	def checkLabel(cls, label):
		if label not in skillTagsJson.keys():
			raise ValueError('Skill label is not allowed')
		return label

class SkillTagInDB(BaseModelWithId, SkillTagBase):
	class Config(BaseModelWithIdConfig):
		schema_extra = {'example': {'label': 'ReacJS'}}
