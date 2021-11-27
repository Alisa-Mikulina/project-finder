from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Body, UploadFile
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from controllers.TokenController import getAuthorizedUser
from controllers.UserController import getUserByUsername
from controllers.MatchController import createMatch, getMatchByBoth, addUserLikeToMatch, addProjectLikeToMatch, getUserMatches, getProjectMatches
from db.mongodb import getDatabase
from models.MatchModel import MatchBase, MatchInDB, MatchCreateReq
from models.ProjectModel import ProjectInDB
from models.UserModel import UserInDB

matchRouter = APIRouter(prefix='/match', tags=['match'])

@matchRouter.post('/user_like', status_code=status.HTTP_201_CREATED, response_model=MatchBase)
async def create(slug: ProjectInDB.slug = Depends(getProjectBySlug), 
                 username: UserInDB.username = Depends(getAuthorizedUser),
                 match: MatchCreateReq = Body(...),
                 db: Database = Depends(getDatabase)):
	predictMatch = getMatchByBoth(db, username, slug)
	if predictMatch:
        if predictMatch.likeFromProject:
            if predictMatch.likeFromUser:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Match already exists')
            else:
                addUserLikeToMatch(db, username, slug)
    createMatch(db, match, username, slug, likeFromUser=True)
	return {**match.dict(), 'slug': slug, 'username': username}

@matchRouter.post('/project_like', status_code=status.HTTP_201_CREATED, response_model=MatchBase)
async def create(slug: ProjectInDB.slug = Depends(getProjectBySlug), 
                 username: UserInDB.username = Depends(getAuthorizedUser),
                 match: MatchCreateReq = Body(...),
                 db: Database = Depends(getDatabase)):
	predictMatch = getMatchByBoth(db, username, slug)
	if predictMatch:
        if predictMatch.likeFromUser:
            if predictMatch.likeFromProject:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Match already exists')
            else:
                addProjectLikeToMatch(db, username, slug)
    createMatch(db, match, username, slug, likeFromProject=True)
	return {**match.dict(), 'slug': slug, 'username': username}

@matchRouter.get('/my_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
async def selfMatches(db: Database = Depends(getDatabase), user: UserInDB = Depends(getAuthorizedUser)):
	matches = getUserMatches(db, user.username)
	return matches

@matchRouter.get('/my_project_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
async def myProjectMatches(db: Database = Depends(getDatabase), project: ProjectInDB = Depends(getProjectBySlug)):
	matches = getProjectMatches(db, project.slug)
	return matches