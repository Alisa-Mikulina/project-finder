from typing import TYPE_CHECKING, Optional, Type
from bson import ObjectId
from pydantic import BaseModel, Field, BaseConfig

class PyObjectId(ObjectId):
	@classmethod
	def __get_validators__(cls):
		yield cls.validate

	@classmethod
	def validate(cls, v):
		if not ObjectId.is_valid(v):
			raise ValueError('Invalid objectid')
		return ObjectId(v)

	@classmethod
	def __modify_schema__(cls, field_schema):
		field_schema.update(type='string')

class MyExtraConfigWithExclusionsAndInclusion(BaseConfig):
	exclude = set()
	include = set()

class MyBaseModelWithExcAndInc(BaseModel):
	if TYPE_CHECKING:
		__config__: Type[MyExtraConfigWithExclusionsAndInclusion] = MyExtraConfigWithExclusionsAndInclusion
	Config = MyExtraConfigWithExclusionsAndInclusion

	def __init__(self, **data):
		excludeSet = self.__config__.exclude
		includeSet = self.__config__.include
		if excludeSet and includeSet:
			raise Exception('Don\'t use exclude and include at the same time')
		if excludeSet:
			self.__class__.__fields__ = {
			    key: value
			    for key, value in self.__class__.__fields__.items() if key not in excludeSet
			}
		if includeSet:
			self.__class__.__fields__ = {
			    key: value
			    for key, value in self.__class__.__fields__.items() if key in includeSet
			}
		super().__init__(**data)

class BaseModelWithId(MyBaseModelWithExcAndInc):
	id: Optional[PyObjectId] = Field(alias='_id')

class BaseModelWithIdConfig:
	allow_population_by_field_name = True
	arbitrary_types_allowed = True
	json_encoders = {ObjectId: str}
