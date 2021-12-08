from fastapi import APIRouter, status, HTTPException, Depends, Body
from pymongo.database import Database
from controllers.ProjectController import getProjectBySlug
from controllers.TokenController import getAuthorizedUser
from controllers.MatchController import *
from controllers.UserController import getUserByUsername
from core.errors import API_ERRORS
from db.mongodb import getDatabase
from models.MatchModel import *
from models.UserModel import UserInDB

matchRouter = APIRouter(prefix='/match', tags=['match'])

@matchRouter.post('/like_user', status_code=status.HTTP_200_OK, response_model=MatchLikeUserRes)
async def create(user: UserInDB = Depends(getAuthorizedUser),
                 match: MatchLikeUserReq = Body(...),
                 db: Database = Depends(getDatabase)):
	predictProject = getProjectBySlug(db, match.slug)
	if not predictProject:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NotFound'])

	if predictProject.user.username != user.username:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NoAccess'])

	predictUser = getUserByUsername(db, match.username)
	if not predictUser:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['user.NotFound'])

	createOrUpdateMatch(db, match.username, match.slug, likeFromProject=True)
	return {}

@matchRouter.post('/like_project', status_code=status.HTTP_200_OK, response_model=MatchLikeProjectRes)
async def create(user: UserInDB = Depends(getAuthorizedUser),
                 match: MatchLikeProjectReq = Body(...),
                 db: Database = Depends(getDatabase)):
	predictProject = getProjectBySlug(db, match.slug)
	if not predictProject:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NotFound'])

	createOrUpdateMatch(db, user.username, match.slug, likeFromUser=True)
	return {}

@matchRouter.get('/my_matches', status_code=status.HTTP_200_OK, response_model=List[MatchGetSelfRes])
async def selfMatches(user: UserInDB = Depends(getAuthorizedUser), db: Database = Depends(getDatabase)):
	matches = getUserMatches(db, user.username)
	return matches

@matchRouter.post('/my_project_matches',
                  status_code=status.HTTP_200_OK,
                  response_model=List[MatchGetSelfProjectRes])
async def myProjectMatches(req: MatchGetSelfProjectReq,
                           user: UserInDB = Depends(getAuthorizedUser),
                           db: Database = Depends(getDatabase)):
	predictProject = getProjectBySlug(db, req.slug)
	if not predictProject:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NotFound'])

	if predictProject.user.username != user.username:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NoAccess'])
	matches = getProjectMatches(db, req.slug)
	return matches
