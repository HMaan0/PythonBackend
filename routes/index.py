from fastapi import APIRouter
from routes.user import router as user_router
from routes.accounts import router as account_router

router = APIRouter()
router.include_router(user_router, prefix="/user")
router.include_router(account_router, prefix="/account")