from fastapi import FastAPI
from core.config import HOST, PORT, DEV
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# TODO: правильно и безопасно настроить корсы при выкатывании в прод
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/test')
async def test_url():
	return {'ok': 'works'}

if (__name__ == '__main__'):
	uvicorn.run('main:app', host=HOST, port=PORT, reload=DEV)
