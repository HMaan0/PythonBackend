from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config import JWT_SECRET

security = HTTPBearer()


async def auth_middleware(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = decoded.get("userId")

        if not user_id:
            raise HTTPException(status_code=403, detail="Incorrect")

        return {"userId": user_id}

    except jwt.PyJWTError as err:
        raise HTTPException(status_code=403, detail=str(err))