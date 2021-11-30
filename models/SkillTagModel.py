from typing import List, Optional
from fastapi.exceptions import HTTPException
from pydantic import Field, validator
from starlette import status
from core.config import skillTagsJson
from core.errors import API_ERRORS
from models.BaseModel import MyBaseModelWithExcAndInc

class SkillTagBase(MyBaseModelWithExcAndInc):
	label: str = Field(min_length=3, max_length=20)

	@validator('label')
	def checkLabel(cls, label):
		if label not in skillTagsJson.keys():
			raise ValueError('Skill label is not allowed')
		return label

class SkillTagList(MyBaseModelWithExcAndInc):
	skillTags: List[SkillTagBase] = Field(default=[])

	@validator('skillTags')
	def checkSkillTags(cls, skillTags):
		skillTagLabels = set()
		for skillTag in skillTags:
			skillTagLabels.add(skillTag.label)
		if len(skillTagLabels) != len(skillTags):
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['skillTag.NotUnique'])
		return skillTags

class SkillTagListRequired(SkillTagList):
	skillTags: List[SkillTagBase] = Field(...)

	@validator('skillTags')
	def checkSkillTags(cls, skillTags):
		if len(skillTags) <= 0:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['skillTag.Required'])
		return super().checkSkillTags(skillTags)

# SkillTag List GET (/api/skill_tag/)
class SkillTagListRes(SkillTagList):
	pass