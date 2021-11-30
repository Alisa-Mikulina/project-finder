from fastapi import Header, UploadFile, File, HTTPException, status
from pymongo.database import Database
from core.config import allowedImageExtensions, uniqueSlugifyRegexp
from slugify import slugify

from core.errors import API_ERRORS

async def getImageFile(file: UploadFile = File(...), content_length: int = Header(..., le=1024**2)):
	fileExtension = file.filename.split('.')[-1]
	if fileExtension not in allowedImageExtensions:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=API_ERRORS['file.FileIsNotAnImage'])
	return file

def slugifyUniqueString(strToSlugify: str):
	return slugify(strToSlugify, lowercase=False, regex_pattern=uniqueSlugifyRegexp)
