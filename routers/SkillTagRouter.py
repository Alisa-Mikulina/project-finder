from fastapi import APIRouter, status
from models.SkillTagModel import *

skillTagRouter = APIRouter(prefix='/skill_tag', tags=['skill_tag'])

@skillTagRouter.get('/', status_code=status.HTTP_200_OK, response_model=SkillTagListRes)
async def listSkillTagsEP():
	return skillTagsJson
