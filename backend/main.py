from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import os

from database import get_db, engine
from models import Base, User, Expense
from schemas import (
    UserRegister, UserLogin, UserResponse, TokenResponse,
    ExpenseCreate, ExpenseResponse, ExpenseListResponse,
    StatsResponse, StatsByCategoryResponse
)
from authentication import (
    get_password_hash, verify_password, create_access_token,
    decode_access_token
)
from dotenv import load_dotenv
import os
load_dotenv()
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")
security = HTTPBearer()

# Default categories
DEFAULT_CATEGORIES = [
    "Food", "Transport", "Entertainment", "Shopping", 
    "Bills", "Healthcare", "Education", "Others"
]

# Dependency to get current user
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Auth Routes
@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/auth/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/logout")
def logout(current_user: User = Depends(get_current_user)):
    # In a stateless JWT system, logout is handled client-side by removing the token
    return {"message": "Successfully logged out"}

# Expense Routes
@app.post("/expense/create_expense", response_model=ExpenseResponse)
def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate category
    if expense_data.category not in DEFAULT_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Must be one of: {', '.join(DEFAULT_CATEGORIES)}"
        )
    
    new_expense = Expense(
        user_id=current_user.id,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        date=datetime.utcnow()
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense

@app.delete("/expense/delete_expense/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
    
    return {"message": "Expense deleted successfully"}

@app.get("/expense/list_expense", response_model=ExpenseListResponse)
def list_expense(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).order_by(Expense.date.desc()).all()  # ✅ Already descending order!
    
    return {"expenses": expenses, "count": len(expenses)}

@app.get("/expense/list_expense_by_category", response_model=ExpenseListResponse)
def list_expense_by_category(
    category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if category not in DEFAULT_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Must be one of: {', '.join(DEFAULT_CATEGORIES)}"
        )
    
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.category == category
    ).order_by(Expense.date.desc()).all()  # ✅ Already descending order!
    
    return {"expenses": expenses, "count": len(expenses)}

# Stats Routes
@app.get("/stats/total", response_model=StatsResponse)
def get_total_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    total = sum(expense.amount for expense in expenses)
    
    return {
        "total_amount": total,
        "total_expenses": len(expenses)
    }

@app.get("/stats/total_by_category", response_model=List[StatsByCategoryResponse])
def get_stats_by_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    
    # Group by category
    category_stats = {}
    for expense in expenses:
        if expense.category not in category_stats:
            category_stats[expense.category] = {
                "amount": 0,
                "count": 0
            }
        category_stats[expense.category]["amount"] += expense.amount
        category_stats[expense.category]["count"] += 1
    
    # Format response
    result = [
        {
            "category": category,
            "total_amount": data["amount"],
            "total_expenses": data["count"]
        }
        for category, data in category_stats.items()
    ]
    
    return result

@app.get("/")
def root():
    return {
        "message": "Expense Tracker API",
        "available_categories": DEFAULT_CATEGORIES
    }

# For Vercel serverless
app = app