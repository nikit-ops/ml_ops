from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.user import User
from services.crud import user as UserService
from services.crud.user import check_password
from typing import List, Dict
import logging
import secrets
from datetime import datetime, timedelta
from database.redis_client import redis_client


logger = logging.getLogger(__name__)

user_route = APIRouter()

@user_route.post(
    '/signup',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with email and password")
async def signup(data: User, session=Depends(get_session)) -> Dict[str, str]:
    """
    Create new user account.

    Args:
        data: User registration data
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user already exists
    """
    try:
        if UserService.get_user_by_email(data.email, session):
            logger.warning(f"Signup attempt with existing email: {data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        user = User(
            email=data.email,
            password=data.password)
        UserService.create_user(user, session)
        logger.info(f"New user registered: {data.email}")
        return {"message": "User successfully registered"}

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@user_route.post('/signin')
async def signin(data: User, session=Depends(get_session)) -> Dict[str, str]:
    """
    Authenticate existing user and return an auth token.

    Args:
        form_data: User credentials
        session: Database session

    Returns:
        dict: Auth token

    Raises:
        HTTPException: If authentication fails
    """
    user = UserService.get_user_by_email(data.email, session)
    if user is None:
        logger.warning(f"Login attempt with non-existent email: {data.email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    if not check_password(user.password, data.password):
        logger.warning(f"Failed login attempt for user: {data.email}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")
    
    
    token = secrets.token_hex(16)
    redis_client.setex(f"auth_token:{token}", timedelta(hours=24), user.id)  
    logger.info(f"User {data.email} signed in successfully with token {token}")
    return {"message": "User signed in successfully", "token": token}

@user_route.get(
    "/get_all_users",
    response_model=List[User],
    summary="Get all users",
    response_description="List of all users"
)
async def get_all_users(session=Depends(get_session), token: str = None):
    """
    Get list of all users.

    Args:
        session: Database session
        token: Auth token (passed as a query parameter)

    Returns:
        List[UserResponse]: List of users

    Raises:
        HTTPException: If token is invalid, expired, or user is not an admin
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required")
    
    user_id = redis_client.get(f"auth_token:{token}")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user = UserService.get_user_by_id(int(user_id), session)
    if not user or not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    
    try:
        users = UserService.get_all_users(session)
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )