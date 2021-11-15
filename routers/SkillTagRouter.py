from typing import List
from fastapi import APIRouter, status, Depends
from pymongo.database import Database
from controllers.SkillTagController import getAllSkillTags
from db.mongodb import getDatabase
from models.SkillTagModel import SkillTagBase

skillTagRouter = APIRouter(prefix='/skill_tag', tags=['skill_tag'])

@skillTagRouter.get('/', status_code=status.HTTP_200_OK, response_model=List[SkillTagBase])
def getSkillTagsList(db: Database = Depends(getDatabase)):
	skillTags = list(map(lambda ob: SkillTagBase(**ob), getAllSkillTags(db)))
	return skillTags
