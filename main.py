from fastapi import FastAPI
from fastapi.param_functions import Depends
from controllers.TokenController import getAuthorizedUser
from core.config import HOST, PORT, DEV
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db.mongodb import closeMongoConnection, connectToMongo
from models.UserModel import UserInDB
from routers.UserRouter import userRouter

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

app.include_router(userRouter, prefix='/user')

@app.get('/test')
async def test_url():
	return {'ok': 'works'}

@app.get('/test_token')
async def text_token(user: UserInDB = Depends(getAuthorizedUser)):
	print(user)
	return {'ok': 'works'}

if (__name__ == '__main__'):
	uvicorn.run('main:app', host=HOST, port=PORT, reload=DEV)
