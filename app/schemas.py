from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from datetime import datetime

# Enum for transaction status
class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# Schema for creating a new transaction
class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be greater than 0")
    description: str = Field(..., min_length=3, max_length=100, description="Description must be between 3 and 100 characters")
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)

# Schema for transaction responses
class Transaction(BaseModel):
    id: str
    amount: float
    description: str
    status: TransactionStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Schema for user responses
class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)

# Schema for authentication token
class Token(BaseModel):
    access_token: str
    token_type: str