import os
from typing import Any
import motor.motor_asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, GetJsonSchemaHandler
from bson import ObjectId

uri = os.getenv("DATABASE_URL") 

client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client["test"]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema, handler: GetJsonSchemaHandler
    ):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class User(BaseModel):
    id: PyObjectId | None = None
    firstName: str
    lastName: str
    password: str
    userName: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class Transactions(BaseModel):
    id: PyObjectId | None = None
    userId: PyObjectId
    balance: float

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


user_collection = db["user"]
transaction_collection = db["transactions"]