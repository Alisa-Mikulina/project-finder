from typing import List, Optional
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from models.MatchModel import MatchInDB

def getMatchByBoth(db: Database, username: str, slug: str):
	match = db.matches.find_one({'slug': slug, 'username': username})
	if match:
		return MatchInDB(**match)
	return

def createOrUpdateMatch(db: Database,
                        username: str,
                        slug: str,
                        likeFromUser: Optional[bool] = False,
                        likeFromProject: Optional[bool] = False):
	predictMatch = getMatchByBoth(db, username, slug)
	project = getProjectBySlug(db, slug)
	if predictMatch:
		db.matches.find_one_and_update({
		    'username': username,
		    'slug': slug
		}, {
		    '$set': {
		        'likeFromUser': likeFromUser or predictMatch.likeFromUser,
		        'likeFromProject': likeFromProject or predictMatch.likeFromProject
		    }
		})
		return
	match = db.matches.insert_one({
	    'username': username,
	    'slug': slug,
	    'projectTitle': project.title,
	    'likeFromUser': likeFromUser,
	    'likeFromProject': likeFromProject
	})
	return MatchInDB(**match)

def getUserMatches(db: Database, username: str):
	matches = db.matches.find({'username': username, 'likeFromUser': True, 'likeFromProject': True})
	return list(map(lambda ob: MatchInDB(**ob), matches))

def getProjectMatches(db: Database, slug: str):
	matches = db.matches.find({'slug': slug, 'likeFromUser': True, 'likeFromProject': True})
	return list(map(lambda ob: MatchInDB(**ob), matches))
