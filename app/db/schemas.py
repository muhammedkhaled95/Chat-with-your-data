from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr = None
    user_folder_name: str
    class Config:
        from_attributes = True


class File(BaseModel):
    filename: str
    file_type: str
    file_path: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogIn(BaseModel):
  email: EmailStr
  password: str


class FileCreate(BaseModel):
    filename: str
    file_type: str
    file_path: str
    

class Token(BaseModel):
    access_token: str
    token_type: str

    
class PasswordResetRequest(BaseModel):
    email: str

class PasswordChangeRequest(BaseModel):
    email: str
    old_password: str
    new_password: str
    
class ResetTokenAndPassword(BaseModel):
    reset_token: str
    new_password: str
    
class UserQuery(BaseModel):
    query: str
    
class LLMAnswer(BaseModel):
    answer: str