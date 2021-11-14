from fastapi import FastAPI
from fastapi.param_functions import Depends
from controllers.TokenController import getAuthorizedUser
from core.config import HOST, PORT, DEV
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from db.mongodb import closeMongoConnection, connectToMongo
from models.UserModel import UserInDB
from routers.UserRouter import userRouter
from routers.AuthRouter import authRouter

app = FastAPI()

# TODO: правильно и безопасно настроить корсы при выкатывании в прод
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connectToMongo)
app.add_event_handler("shutdown", closeMongoConnection)

app.mount('/media', StaticFiles(directory="media"), name="media")

app.include_router(userRouter, prefix='/api')
app.include_router(authRouter, prefix='/api')

@app.get('/test')
async def test_url():
	return {'ok': 'works'}

@app.get('/test_token')
async def text_token(user: UserInDB = Depends(getAuthorizedUser)):
	return {'ok': 'works'}

if (__name__ == '__main__'):
	uvicorn.run('main:app', host=HOST, port=PORT, reload=DEV)
