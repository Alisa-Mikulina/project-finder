from typing import List, Optional
from pymongo.database import Database
from models.UserModel import UserInDB
from models.ProjectModel import ProjectInDB
from models.MatchModel import MatchInDB

def createMatch(db: Database, match: MatchInDB, username: str, slug: str, likeFromUser: Optional[bool], likeFromProject: Optional[bool]):
    newMatch = MatchInDB(**{**match.dict(), 'username': username, 'slug': slug, 'likeFromUser': likeFromUser, 'likeFromProject': likeFromProject})
    db.matches.insert_one(newMatch.dict())

def getMatchByBoth(db: Database, username: str, slug: str):
    match = MatchInDB.matches.find_one({'slug': slug}, {'username': username})
    if match:
        return MatchInDB(**match)

def addUserLikeToMatch(db: Database, username: str, slug: str):
    match = getMatchByBoth(db, username, slug)
    if match:
        match.likeFromUser = True
    return

def addProjectLikeToMatch(db: Database, username: str, slug: str):
    match = getMatchByBoth(db, username, slug)
    if match:
        match.likeFromProject = True
    return

def getUserMatches(db: Database, username: str):
    matches = db.matches.find({'username': username})
    if matches:
        return list(map(lambda ob: ProjectInDB(**ob), matches))

def getProjectMatches(db: Database, slug: str):
    matches = db.matches.find({'slug': slug})
    if matches:
        return list(map(lambda ob: ProjectInDB(**ob), matches))