import pytest
from sqlalchemy.orm.session import Session
from app.models import User, Transaction
from app.schemas import TransactionStatus
from datetime import datetime, UTC


def test_create_transaction(db_session):
    user = User(username="testuser", email="test@example.com", hashed_password="hashedpass")
    db_session.add(user)
    db_session.commit()

    transaction = Transaction(
        amount=100.0,
        description="Test transaction",
        status=TransactionStatus.PENDING,
        created_at=datetime.now(UTC),
        user_id=user.id
    )
    db_session.add(transaction)
    db_session.commit()

    assert transaction.id is not None
    assert transaction.amount == 100.0
    assert transaction.description == "Test transaction"
    assert transaction.status == TransactionStatus.PENDING
    assert transaction.user_id == user.id
