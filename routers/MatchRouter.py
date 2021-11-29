from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Body, UploadFile
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from controllers.TokenController import getAuthorizedUser
from controllers.UserController import getUserByUsername
from controllers.MatchController import createOrUpdateMatch, getMatchByBoth, getUserMatches, getProjectMatches
from db.mongodb import getDatabase
from models.MatchModel import MatchBase, MatchInDB, MatchCreateReq
from models.ProjectModel import ProjectInDB
from models.UserModel import UserInDB

matchRouter = APIRouter(prefix='/match', tags=['match'])

@matchRouter.post('/user_like', status_code=status.HTTP_201_CREATED, response_model=MatchBase)
async def create(project: ProjectInDB = Depends(getProjectBySlug), 
                 user: UserInDB = Depends(getAuthorizedUser),
                 match: MatchCreateReq = Body(...),
                 db: Database = Depends(getDatabase)):
        slug = project.slug
        username = user.username
        predictMatch = getMatchByBoth(db, username, slug)
        if predictMatch and predictMatch.likeFromProject and predictMatch.likeFromUser:
                return
        createOrUpdateMatch(db, username, slug, likeFromUser=True)
        return {**match.dict(), 'slug': slug, 'username': username}

@matchRouter.post('/project_like', status_code=status.HTTP_201_CREATED, response_model=MatchBase)
async def create(project: ProjectInDB = Depends(getProjectBySlug), 
                 user: UserInDB = Depends(getAuthorizedUser),
                 match: MatchCreateReq = Body(...),
                 db: Database = Depends(getDatabase)):
        slug = project.slug
        username = user.username
        predictMatch = getMatchByBoth(db, username, slug)
        if predictMatch and predictMatch.likeFromUser and predictMatch.likeFromProject:
                return
        createOrUpdateMatch(db, username, slug, likeFromProject=True)
        return {**match.dict(), 'slug': slug, 'username': username}

@matchRouter.get('/my_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
async def selfMatches(db: Database = Depends(getDatabase), user: UserInDB = Depends(getAuthorizedUser)):
	matches = getUserMatches(db, user.username)
	return matches

@matchRouter.get('/my_project_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
async def myProjectMatches(db: Database = Depends(getDatabase), project: ProjectInDB = Depends(getProjectBySlug)):
	matches = getProjectMatches(db, project.slug)
	return matches