from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List
import uuid
from . import models, schemas, crud, auth
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI()

# Route to create a new user
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Route to authenticate and get access token
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Route to get current user's information
@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

# Route to create a new transaction
@app.post("/transactions/", response_model=schemas.Transaction)
async def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        db_transaction = models.Transaction(
            id=str(uuid.uuid4()),
            amount=transaction.amount,
            description=transaction.description,
            status=schemas.TransactionStatus.PENDING,
            created_at=datetime.now(timezone.utc)
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Route to get all transactions
@app.get("/transactions/", response_model=List[schemas.Transaction])
async def read_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()

# Route to get a specific transaction by ID
@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
async def read_transaction(transaction_id: str, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

# Route to update a transaction's status
@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
async def update_transaction(transaction_id: str, status: schemas.TransactionStatus, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db_transaction.status = status
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Test route
@app.get("/test")
async def test_route():
    return {"message": "Test route is working"}