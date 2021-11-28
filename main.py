from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.param_functions import Body, Depends
from starlette.responses import JSONResponse
from controllers.TokenController import getAuthorizedUser
from core.config import HOST, PORT, DEV
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from db.mongodb import closeMongoConnection, connectToMongo
from models.UserModel import UserInDB
from routers.UserRouter import userRouter
from routers.AuthRouter import authRouter
from routers.SkillTagRouter import skillTagRouter
from routers.ProjectRouter import projectRouter
from routers.MatchRouter import matchRouter

app = FastAPI()

# TODO: правильно и безопасно настроить корсы при выкатывании в прод
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_event_handler('startup', connectToMongo)
app.add_event_handler('shutdown', closeMongoConnection)

app.mount('/media', StaticFiles(directory='media'), name='media')

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(req, exc):
	return JSONResponse([exc.detail], status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def http_validation_error_handler(req, exc):
	return JSONResponse([{
	    'errorCode': -1,
	    'msg': f'{".".join(list(map(str,error["loc"])))}:{error["msg"]}'
	} for error in exc.errors()],
	                    status_code=422)

app.include_router(userRouter, prefix='/api')
app.include_router(authRouter, prefix='/api')
app.include_router(skillTagRouter, prefix='/api')
app.include_router(projectRouter, prefix='/api')
app.include_router(matchRouter, prefix='/api')

@app.get('/test')
async def test_url():
	return {'ok': 'works'}

@app.get('/test_token')
async def text_token(user: UserInDB = Depends(getAuthorizedUser)):
	return {'ok': 'works'}

if (__name__ == '__main__'):
	uvicorn.run('main:app', host=HOST, port=PORT, reload=DEV)
