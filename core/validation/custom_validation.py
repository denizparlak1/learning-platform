from bson import ObjectId
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not isinstance(v, (ObjectId, str)):
            raise ValueError("ObjectId must be a valid ObjectId or a string")
        return ObjectId(v) if isinstance(v, str) else v
