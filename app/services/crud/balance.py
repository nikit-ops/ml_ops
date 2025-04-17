from sqlalchemy.orm import Session
from sqlalchemy import select
from models.balance import Balance
from models.transaction import Transaction, TransactionType


def create_balance(session: Session, user_id: int, initial_amount: float = 0.0) -> Balance:
    """Automatically create a balance for a user if it doesn't exist."""
    statement = select(Balance).where(Balance.user_id == user_id)
    existing_balance = session.execute(statement).scalar_one_or_none()
    if existing_balance:
        return existing_balance

    balance = Balance(user_id=user_id, amount=initial_amount)
    session.add(balance)
    session.refresh(balance)

    transaction = Transaction(
        user_id=user_id,
        amount=initial_amount,
        type=TransactionType.DEPOSIT,
        description="Initial balance creation"
    )
    session.add(transaction)
    session.commit()
    return balance


def get_balance_by_id(session: Session, balance_id: int) -> Balance:
    """Retrieve a balance by its ID."""
    statement = select(Balance).where(Balance.id == balance_id)
    result = session.execute(statement).scalar_one_or_none()
    return result


def get_balance_by_user_id(session: Session, user_id: int) -> Balance:
    """Retrieve a balance by user ID."""
    statement = select(Balance).where(Balance.user_id == user_id)
    result = session.execute(statement).scalar_one_or_none()
    return result


def deposit(session: Session, balance_id: int, amount: float) -> Balance:
    """Deposit funds into the balance."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    balance = get_balance_by_id(session, balance_id)
    if not balance:
        raise ValueError(f"Balance with ID {balance_id} not found.")

    balance.amount += amount
    session.add(balance)
    session.refresh(balance)

    transaction = Transaction(
        user_id=balance.user_id,
        amount=amount,
        type=TransactionType.DEPOSIT,
        description="Deposit"
    )
    session.add(transaction)
    session.commit()
    return balance


def withdraw(session: Session, balance_id: int, amount: float) -> Balance:
    """Withdraw funds from the balance."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    balance = get_balance_by_id(session, balance_id)
    if not balance:
        raise ValueError(f"Balance with ID {balance_id} not found.")

    if balance.amount < amount:
        raise ValueError("Insufficient funds")

    balance.amount -= amount
    session.add(balance)
    session.commit()
    session.refresh(balance)

    transaction = Transaction(
        user_id=balance.user_id,
        amount=-amount,
        type=TransactionType.WITHDRAWAL,
        description="Withdrawal"
    )
    session.add(transaction)
    session.commit()
    return balance