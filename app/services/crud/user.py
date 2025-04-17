import re
import bcrypt
from models.user import User
from models.balance import Balance
from typing import List, Optional

def get_all_users(session) -> List[User]:
    return session.query(User).all()

def get_user_by_id(id:int, session) -> Optional[User]:
    users = session.get(User, id) 
    if users:
        return users 
    return None

def get_user_by_email(email:str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user 
    return None

def validate_email(email: str) -> None:
    """Validate the format of an email."""
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not email_pattern.match(email):
        raise ValueError("Invalid email format")

def validate_password(password: str) -> None:
    """Validate the minimum length of a password."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(hashed_password: str, password: str) -> bool:
    """Check if a password matches its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_user(user: User, session, is_admin: bool = False) -> User:
    """
    Create a new user with email and password validation, and initialize their balance.

    Args:
        user: User object containing email and password
        session: Database session
        is_admin: Boolean flag to set the user as an admin

    Returns:
        User: The created user object
    """
    validate_email(user.email)
    validate_password(user.password)
    user.password = hash_password(user.password)
    user.is_admin = is_admin  # Set the is_admin flag

    session.add(user)
    session.refresh(user)

    balance = Balance(user_id=user.id, amount=0.0)
    session.add(balance)
    session.commit()

    return user