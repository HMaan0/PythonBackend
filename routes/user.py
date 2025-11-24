from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from schemas.user_schema import SignInSchema
from db import user_collection, transaction_collection
from middleware import auth_middleware
from bson import ObjectId
import jwt
from config import JWT_SECRET
import random

router = APIRouter()


@router.post("/signup")
async def signup(user: SignInSchema):
    user_data = user.dict()

    try:
        existing_user = await user_collection.find_one(
            {"userName": user_data["userName"]}
        )
        if existing_user:
            return JSONResponse(
                content={"msg": "User Name Already Exist's into Database."}
            )

        new_user = await user_collection.insert_one(user_data)
        user_id = new_user.inserted_id

        balance = 1 + random.random() * 10000

        await transaction_collection.insert_one(
            {"userId": user_id, "balance": balance}
        )

        token = jwt.encode({"userId": str(user_id)}, JWT_SECRET, algorithm="HS256")

        return JSONResponse(
            content={"msg": "User Created Successfully", "token": token}
        )

    except Exception as err:
        return JSONResponse(content={"msg": str(err)})


@router.get("/")
async def home():
    return {"msg": "Wokring"}


@router.post("/signin")
async def signin(data: dict):
    username = data.get("username")
    password = data.get("password")

    try:
        user = await user_collection.find_one({"userName": username})

        if not user:
            return JSONResponse(content={"msg": "No Username/Password Found"})

        if user["password"] == password:
            token = jwt.encode(
                {"userId": str(user["_id"])}, JWT_SECRET, algorithm="HS256"
            )
            return JSONResponse(
                content={
                    "msg": "Logged in Successfully",
                    "token": token,
                    "firstName": user["firstName"],
                }
            )

        return JSONResponse(content={"msg": "Incorrect Password"})

    except Exception as err:
        return JSONResponse(content={"msg": str(err)})


@router.put("/")
async def update_user(
    updated_user: dict, user=Depends(auth_middleware)
):
    user_id = user["userId"]
    try:
        await user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": updated_user}
        )
        return JSONResponse(content={"msg": "Updated Successfully"})
    except Exception as err:
        return JSONResponse(content={"msg": str(err)})


@router.get("/bulk")
async def bulk(filter: str = Query(default="")):
    try:
        regex = {"$regex": filter, "$options": "i"}
        cursor = user_collection.find({"$or": [{"firstName": regex}, {"lastName": regex}]})
        users = await cursor.to_list(length=None)
        print(cursor)

        user_response = [
            {
                "username": u["userName"],
                "firstName": u["firstName"],
                "lastName": u["lastName"],
                "_id": str(u["_id"]),
            }
            for u in users
        ]

        return {"user": user_response}

    except Exception:
        return JSONResponse(
            content={"msg": "Error In Finding User from Database"}
        )