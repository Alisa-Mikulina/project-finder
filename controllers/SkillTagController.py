from pymongo.database import Database
from models.SkillTagModel import SkillTagInDB
from core.config import skillTagsJson

def checkSkillTagsInDB(db: Database):
	skillTagsInDB = getAllSkillTags(db)
	skillTagsChecked = {key: False for key in skillTagsJson.keys()}
	skillTagsToAdd = []

	for skillTag in skillTagsInDB:
		skillTagsChecked[skillTag['label']] = True

	for key in skillTagsChecked:
		if not skillTagsChecked[key]:
			skillTagsToAdd.append(SkillTagInDB(**{'label': key}).dict())

	if skillTagsToAdd:
		db.skillTags.insert_many(skillTagsToAdd)

def getAllSkillTags(db: Database):
	return db.skillTags.find({})