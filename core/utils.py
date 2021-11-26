from fastapi import Header, UploadFile, File, HTTPException, status
from pymongo.database import Database
from core.config import allowdImageExtensions
from slugify import slugify

from core.errors import API_ERRORS

async def getImageFile(file: UploadFile = File(...), content_length: int = Header(..., le=1024**2)):
	fileExtension = file.filename.split('.')[-1]
	if fileExtension not in allowdImageExtensions:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['file.FileIsNotAnImage'])
	return file

def slugifyString(strToSlugify: str, lowercase: bool):
	return slugify(strToSlugify, lowercase=lowercase, separator='_')