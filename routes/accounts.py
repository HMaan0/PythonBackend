from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from middleware import auth_middleware
from db import transaction_collection, client
from bson import ObjectId
from schemas.user_schema import TransferSchema

router = APIRouter()


@router.get("/balance")
async def get_balance(user=Depends(auth_middleware)):
    try:
        result = await transaction_collection.find_one({"userId": ObjectId(user["userId"])})
        if not result:
            return JSONResponse(content={"msg": "Account not found"})
        return JSONResponse(content={"msg": result["balance"]})
    except Exception as err:
        return JSONResponse(content={"msg": str(err)})


@router.post("/transfer")
async def transfer(data: TransferSchema, user=Depends(auth_middleware)):
    amount = data.amount
    to = data.to

    session = await client.start_session()
    session.start_transaction()

    try:
        from_account = await transaction_collection.find_one(
            {"userId": ObjectId(user["userId"])}, session=session
        )

        if not from_account or from_account["balance"] < amount:
            await session.abort_transaction()
            return JSONResponse(content={"msg": "Insufficient Funds"})

        to_account = await transaction_collection.find_one(
            {"userId": ObjectId(to)}, session=session
        )

        if not to_account:
            await session.abort_transaction()
            return JSONResponse(content={"msg": "Invalid Account"})

        await transaction_collection.update_one(
            {"userId": ObjectId(user["userId"])},
            {"$inc": {"balance": -amount}},
            session=session,
        )

        await transaction_collection.update_one(
            {"userId": ObjectId(to)},
            {"$inc": {"balance": amount}},
            session=session,
        )

        await session.commit_transaction()
        return JSONResponse(content={"msg": "Transfer Successful"})

    except Exception as err:
        await session.abort_transaction()
        return JSONResponse(content={"msg": str(err)})

    finally:
        await session.end_session()
    amount = req.get("amount")
    to = req.get("to")

    session = await client.start_session()
    session.start_transaction()

    try:
        from_account = await transaction_collection.find_one(
            {"userId": ObjectId(user["userId"])}, session=session
        )

        if not from_account or from_account["balance"] < amount:
            await session.abort_transaction()
            return JSONResponse(content={"msg": "Insufficient Funds"})

        to_account = await transaction_collection.find_one(
            {"userId": ObjectId(to)}, session=session
        )

        if not to_account:
            await session.abort_transaction()
            return JSONResponse(content={"msg": "Invalid Account"})

        await transaction_collection.update_one(
            {"userId": ObjectId(user["userId"])},
            {"$inc": {"balance": -amount}},
            session=session,
        )

        await transaction_collection.update_one(
            {"userId": ObjectId(to)}, {"$inc": {"balance": amount}}, session=session
        )

        await session.commit_transaction()
        return JSONResponse(content={"msg": "Transfer Successful"})

    except Exception as err:
        await session.abort_transaction()
        return JSONResponse(content={"msg": str(err)})

    finally:
        await session.end_session()