from sqlalchemy.orm import Session
from . import models, schemas, auth

# Function to get a user by their ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Function to get a user by their email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Function to create a new user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to create a new transaction
def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Function to get transactions, optionally filtered by user_id
def get_transactions(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(models.Transaction)
    if user_id:
        query = query.filter(models.Transaction.user_id == user_id)
    return query.offset(skip).limit(limit).all()
