from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core import security
from sqlalchemy.orm import Session
from app.db.models import User
from app.db import crud


# Creates a CryptContext object for handling password hashing and verification using the pbkdf2_sha256 algorithm.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    This module provides security-related functionalities for the FastAPI application.

    Functions:
        create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
            Creates a JSON Web Token (JWT) for a given subject with an optional expiration time.

            Args:
                subject (Union[str, Any]): The subject for which the token is being created. Typically, this is the user identifier.
                expires_delta (timedelta, optional): The time duration after which the token will expire. If not provided, the default expiration time from settings will be used.

            Returns:
                str: The encoded JWT as a string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc)+ expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a password using the application's password context.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_reset_token(email: str) -> str:
    """
    Creates a password reset token for a given email address.

    Args:
        email (str): The email address for which the reset token is being created.

    Returns:
        str: The reset token.
    """
    to_encode = {"email": email}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_reset_token(token: str) -> str:
    """
    Verifies a password reset token.

    Args:
        token (str): The token to verify.

    Returns:
        str: The email address associated with the token.
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"decoded_token = {decoded_token}")
        print(f"decoded_token.get('email') = {decoded_token.get('email')}")
        return decoded_token.get("email")
    except:
        return None


async def user_authenticate(db: Session, email: str, password: str):
    """
    Authenticate a user by their email and password.

    Args:
        db (Session): The database session to use for querying the user.
        email (str): The email address of the user attempting to authenticate.
        password (str): The password provided by the user for authentication.

    Returns:
        User: The authenticated user object if authentication is successful.

    Raises:
        HTTPException: If the email does not exist or the password is incorrect.
    """
    print(f"email = {email}")
    user = await crud.get_user_by_email(db, email)
    print(f"user in user_authenticate = {user}")
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password");
    if not security.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password");
    return user