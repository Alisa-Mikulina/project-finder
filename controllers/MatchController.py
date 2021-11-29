from typing import List, Optional
from pymongo.database import Database
from models.MatchModel import MatchInDB


def getMatchByBoth(db: Database, username: str, slug: str):
    match = db.matches.find_one({'slug': slug}, {'username': username})
    if match:
        return db(**match)

def createOrUpdateMatch(db: Database, username: str, slug: str, likeFromUser: Optional[bool], likeFromProject: Optional[bool]):
    predictMatch = getMatchByBoth(db, username, slug)
    if predictMatch:
            db.matches.find_one_and_update({'username': username}, {'slug': slug}, {'likeFromUser': likeFromUser}, {'likeFromProject': likeFromProject})
            pass
    db.matches.insert_one({'username': username, 'slug': slug, 'likeFromUser': likeFromUser, 'likeFromProject': likeFromProject})

def getUserMatches(db: Database, username: str):
    matches = db.matches.find({'username': username})
    if matches:
        return list(map(lambda ob: MatchInDB(**ob), matches))

def getProjectMatches(db: Database, slug: str):
    matches = db.matches.find({'slug': slug})
    if matches:
        return list(map(lambda ob: MatchInDB(**ob), matches))