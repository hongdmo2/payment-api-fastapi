from sqlalchemy import func, Boolean, Column, Integer, String, Float, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .schemas import TransactionStatus
import uuid

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship to Transaction model
    transactions = relationship("Transaction", back_populates="user")

# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to User model
    user = relationship("User", back_populates="transactions")