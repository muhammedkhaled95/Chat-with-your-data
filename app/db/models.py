from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_folder_name= Column(String, nullable=False, unique=True)
    files = relationship("File", back_populates="owner")  # Relationship to the File table


# File Model
class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String)
    file_type = Column(String)
    file_path = Column(String)  # Path to the file on the server
    uploaded_at = Column(DateTime, default=datetime.now(timezone.utc))
    owner = relationship("User", back_populates="files")  # Relationship to the User table
