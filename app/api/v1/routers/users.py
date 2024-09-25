from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.db import models, schemas
from app.api.v1.dependencies.deps import get_current_user, get_db
from app.db import crud
from sqlalchemy.orm import Session
from app.core import security

users_router = APIRouter(prefix="", tags=["Users"])

"""
Endpoint to retrieve the current authenticated user's information.

This endpoint returns the details of the currently authenticated user.

Args:
    current_user (schemas.User): The current authenticated user, obtained via dependency injection.

Returns:
    schemas.User: The current authenticated user's information.
"""
@users_router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    print(f"current_user = {current_user}")
    return current_user

@users_router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (schemas.UserCreate): The user data to create a new user, including email and password.
        db (Session): The database session to use for the operation.

    Returns:
        models.User: The newly created user object.

    This function performs the following steps:
    1. Hashes the user's password.
    2. Creates a new user instance with the provided email and hashed password.
    3. Adds the new user to the database session.
    4. Commits the transaction to save the new user in the database.
    5. Refreshes the database session to reflect the new user data.
    6. Returns the newly created user object.
    """
    if await crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = await crud.create_user(db, user)
    return db_user


@users_router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session to use for querying the user.

    Returns:
        models.User: The user object with the specified ID.

    Raises:
        HTTPException: Raised if no user is found with the specified ID.
    """
    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.get("/users/email/{email}", response_model=schemas.User)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The database session to use for querying the user.

    Returns:
        models.User: The user object with the specified email address.

    Raises:
        HTTPException: Raised if no user is found with the specified email address.
    """
    db_user = await crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.get("/users", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of users.

    Args:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.
        db (Session): The database session to use for querying the users.

    Returns:
        List[models.User]: A list of user objects.
    """
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@users_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): The database session to use for the operation.

    Raises:
        HTTPException: Raised if no user is found with the specified ID.
    """
    db_user = await crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return

@users_router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.
        user (schemas.UserCreate): The updated user data.
        db (Session): The database session to use for the operation.

    Returns:
        models.User: The updated user object.

    Raises:
        HTTPException: Raised if no user is found with the specified ID.
    """
    db_user = await crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.post("/users/change_password", response_model=schemas.User)
async def change_password(email: str = Form(...),
                          old_password: str = Form(...),
                          new_password: str = Form(...), 
                          db: Session = Depends(get_db), 
                          current_user: schemas.User = Depends(get_current_user)):
    password_data = schemas.PasswordChangeRequest(email=email, old_password=old_password, new_password=new_password)
    print(f"password_data = {password_data}")
    """
    Change a user's password.

    Args:
        user_id (int): The ID of the user to update.
        password_data (schemas.PasswordChangeRequest): The old and new password data.
        db (Session): The database session to use for the operation.
        current_user (schemas.User): The current authenticated user, obtained via dependency injection.

    Returns:
        models.User: The updated user object.

    Raises:
        HTTPException: Raised if no user is found with the specified ID, if the current user is not the owner of the account, or if the old password is incorrect.
    """
    db_user = await crud.get_user(db, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the old password
    if not security.verify_password(password_data.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Change the password
    db_user = await crud.change_password(db, password_data.email, password_data.new_password)
    return db_user
