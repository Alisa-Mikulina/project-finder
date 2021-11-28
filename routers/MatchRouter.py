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

@matchRouter.post('/like_user', status_code=status.HTTP_201_CREATED, response_model=MatchLikeUserRes)
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

@matchRouter.post('/like_project', status_code=status.HTTP_201_CREATED, response_model=MatchLikeProjectRes)
async def create(user: UserInDB = Depends(getAuthorizedUser),
                 match: MatchLikeProjectReq = Body(...),
                 db: Database = Depends(getDatabase)):
	predictProject = getProjectBySlug(db, match.slug)
	if not predictProject:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['project.NotFound'])

	createOrUpdateMatch(db, user.username, match.slug, likeFromUser=True)
	return {}

# @matchRouter.get('/my_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
# async def selfMatches(db: Database = Depends(getDatabase), user: UserInDB = Depends(getAuthorizedUser)):
# 	matches = getUserMatches(db, user.username)
# 	return matches

# @matchRouter.get('/my_project_matches', status_code=status.HTTP_201_CREATED, response_model=List[MatchBase])
# async def myProjectMatches(db: Database = Depends(getDatabase),
#                            project: ProjectInDB = Depends(getProjectBySlug)):
# 	matches = getProjectMatches(db, project.slug)
# 	return matches