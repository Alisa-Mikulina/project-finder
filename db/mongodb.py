from copy import Error
from pymongo import MongoClient
import pymongo
from pymongo.database import Database
from core.config import MONGO_URL

client = None

async def getDatabase() -> Database:
	global client
	return client['project_finder']

async def connectToMongo():
	global client
	client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=1000)
	try:
		client.admin.command('ping')
	except pymongo.errors.ConnectionFailure:
		print('Bad connecton to server')
		raise Error

async def closeMongoConnection():
	global client
	client.close()
