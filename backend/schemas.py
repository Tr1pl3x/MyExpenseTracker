from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Expense Schemas
class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0)
    category: str
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str
    description: Optional[str]
    date: datetime
    
    class Config:
        from_attributes = True

class ExpenseListResponse(BaseModel):
    expenses: List[ExpenseResponse]
    count: int

# Stats Schemas
class StatsResponse(BaseModel):
    total_amount: float
    total_expenses: int

class StatsByCategoryResponse(BaseModel):
    category: str
    total_amount: float
    total_expenses: int