from pydantic import BaseModel, EmailStr, Field

class TransferSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to transfer")
    to: str = Field(..., description="Recipient user ID")

class SignInSchema(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=30)
    lastName: str = Field(..., min_length=1, max_length=30)
    userName: EmailStr 
    password: str = Field(..., min_length=8, max_length=30)