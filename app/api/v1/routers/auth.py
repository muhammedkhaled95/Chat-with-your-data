from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.config import settings
from app.db import crud, models, schemas
from app.api.v1.dependencies.deps import get_db, get_current_user
from app.core import security
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_router = APIRouter(prefix="", tags=["User Authentication"])


@auth_router.post("/login", response_model=schemas.Token)
async def user_login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """
    Endpoint to handle user login.
    This endpoint allows a user to log in by providing their credentials. If the credentials are valid, 
    an access token is generated and returned.
    
    Args:
        user_credentials (OAuth2PasswordRequestForm): The user's login credentials.
        db (Session, optional): The database session dependency.
    
    Returns:
        dict: A dictionary containing the access token and token type.
    
    Raises:
        HTTPException: If the provided credentials are incorrect, an HTTP 400 error is raised.
    """
    user = await security.user_authenticate(db, email=user_credentials.username, password=user_credentials.password)
    print(f"user = {user}")
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/signup", response_model=schemas.User)
async def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate):
    """
    Endpoint to create a new user.

    This endpoint allows a new user to sign up by providing the necessary user details.
    If the user already exists, it redirects the user to the login endpoint.

    Args:
        db (Session): Database session dependency.
        user_in (schemas.UserCreate): User creation schema containing the user details.

    Returns:
        schemas.User: The created user object if the user does not already exist.
        RedirectResponse: Redirects to the login endpoint if the user already exists.
    """
    # if the user alread exists, redirect the user to the login endpoint.
    user = await crud.get_user_by_email(db, email=user_in.email)
    if user:
        return RedirectResponse(url="/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    user = crud.create_user(db, user=user_in)
    return user


@auth_router.post("/reset_password_request")
async def reset_password_request(*, db: Session = Depends(get_db), reset_email: schemas.PasswordResetRequest):
    """
    Endpoint to request a password reset.

    This endpoint allows a user to request a password reset by providing their email address.
    If the email is associated with a user in the database, a reset token will be generated and returned.

    Args:
        db (Session): Database session dependency.
        reset_email (schemas.PasswordResetRequest): The email address for which the password reset is requested.

    Returns:
        dict: A dictionary containing the reset token.

    Raises:
        HTTPException: If the user with the provided email is not found, a 404 status code is returned.
    """
    user = await crud.get_user_by_email(db, email=reset_email.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    reset_token = security.create_reset_token(reset_email.email)
    return {"reset_token": reset_token}


@auth_router.post("/reset_password")
async def reset_password(*, db: Session = Depends(get_db), reset_token_and_password: schemas.ResetTokenAndPassword):
    """
    Endpoint to reset a user's password.

    This endpoint allows a user to reset their password using a reset token and a new password. 
    The reset token is verified, and if valid, the user's password is updated in the database.

    Args:
        db (Session): Database session dependency.
        reset_token_and_password (schemas.ResetTokenAndPassword): Object containing the reset token and the new password.

    Raises:
        HTTPException: If the reset token is invalid (400 Bad Request).
        HTTPException: If the user is not found (404 Not Found).

    Returns:
        dict: A message indicating that the password was updated successfully.
    """
    email = security.verify_reset_token(reset_token_and_password.reset_token)
    print(f"email = {email}")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user = await crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_password_hash = security.get_password_hash(reset_token_and_password.new_password)
    user.hashed_password = new_password_hash
    db.commit()
    return {"message": "Password updated successfully"}
