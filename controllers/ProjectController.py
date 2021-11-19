from typing import List
from pymongo.database import Database
from models.ProjectModel import ProjectBase, ProjectChangeReq, ProjectCreateReq, ProjectInDB
from models.UserModel import UserInDB

def createProject(db: Database, project: ProjectBase, slug: str, user: UserInDB):
	newProject = ProjectInDB(**{**project.dict(), 'slug': slug, 'user': user.dict()})
	db.projects.insert_one(newProject.dict())

def getProjectBySlug(db: Database, slug: str):
	project = db.projects.find_one({'slug': slug})
	if project:
		return ProjectInDB(**project)

def getSelfProjects(db: Database, username: str):
	projects = db.projects.find({'user.username': username})
	return list(map(lambda ob: ProjectInDB(**ob), projects))

def updateProject(db: Database, slug: str, projectChange: ProjectChangeReq):
	project = db.projects.find_one_and_update({'slug': slug}, {'$set': projectChange.dict()})
	return project

def getProjectsBySkillTags(db: Database, skillTags: List[str]):
	projects = db.projects.find({'skillTags.name': {'$in': skillTags}})
	return list(map(lambda ob: ProjectInDB(**ob), projects))