from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.schemas import UserCreate, FileCreate, User, File
from app.core import security
from fastapi import HTTPException, status
import uuid
import os
from pathlib import Path
from app.core.config import settings  # Import settings from the configuration module

async def get_user(db: Session, user_id: int):
    print(f"user_id inside crud.get_user = {user_id}")
    return db.query(models.User).filter(models.User.id == user_id).first()

async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

async def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session to use for the operation.
        user (UserCreate): The user data to create a new user, including email and password.

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
    hashed_password: str = security.get_password_hash(user.password)
    # Define the path for the user's folder
    unique_user_folder_name: str = str(uuid.uuid4()) 
    user_folder: str = os.path.join(Path(settings.BASE_DIR), unique_user_folder_name)

    vector_store_folder_name: str = "vector_store"
    vector_store_folder: str = os.path.join(user_folder, vector_store_folder_name)    
    
    # Create the directory for user folder and user vector store folder inside of it if it does not exist
    Path(user_folder).mkdir(parents=True, exist_ok=True)
    Path(vector_store_folder).mkdir(parents=True, exist_ok=True)
    
    db_user = models.User(username=user.email, email=user.email, hashed_password=hashed_password,
                          user_folder_name=unique_user_folder_name)
    print(f"db_user = {db_user}")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


async def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user.email
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

async def change_password(db: Session, email: str, new_password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db_user.hashed_password = security.get_password_hash(new_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


async def create_file(db: Session, file: FileCreate, user_id: int):
    db_file = models.File(**file.model_dump(), user_id=user_id)
    print(f"db_file = {db_file}")
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


async def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()


async def get_files(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.File).filter(models.File.user_id == user_id).offset(skip).limit(limit).all()


async def delete_file(db: Session, file_id: int):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
        return db_file
    return None


async def update_file(db: Session, file_id: int, file: FileCreate):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file:
        db_file.filename = file.filename
        db_file.file_type = file.file_type
        db.commit()
        db.refresh(db_file)
        return db_file
    return None


async def get_user_files(db: Session, user_id: int):
    return db.query(models.File).filter(models.File.user_id == user_id).all()

async def get_user_folder_name(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().user_folder_name