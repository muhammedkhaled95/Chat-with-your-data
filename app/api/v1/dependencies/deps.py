from app.db.database import SessionLocal  # Import SessionLocal from the appropriate module
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.db import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
get_db(): is a function called to get a session to the DB everytime we get a request through our APIs that needs
to talk to the database, so we can call as much as we want, and after that close the session.

While returning the session instance and closing it manually in the caller is possible, using a 
generator function with yield provides automatic resource management, reduces the risk of forgetting to close the session, 
maintains separation of concerns, and integrates well with modern web frameworks. 
This pattern simplifies code management and ensures that resources are handled consistently and correctly.

In web frameworks like FastAPI, the get_db function is called a "dependency" because it provides a necessary resource
(in this case, a database session) to other parts of the application, such as route handlers or other functions.
Dependencies are used to manage and inject required resources or services into various components of an application.

Separation of Concerns: Using dependencies helps separate the concerns of resource management from the business logic of your application .
Route handlers or other functions don’t need to know how to create or manage the database session;
they only need to use it. This makes the code more modular, maintainable, and testable.
"""
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


#The endpoint that uses get_current_user must pass the token and token type in the Authorization header of the request.
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print(f"inside get_current_user")
    """
    Get the current user from the database based on the provided access token.
    
    Args:
        db (Session): The database session to use for querying the user.
        token (str): The access token provided in the request header.
    
    Returns:
        User: The authenticated user object if the token is valid.
    
    Raises:
        HTTPException: If the token is invalid or expired, a 401 status code is returned.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        print(f"user_id = {user_id}")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    print(f"user at the end of get_current_user = {user}")
    return user