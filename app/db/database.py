#This file is to handle database communication with sqlalchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#Providing the database url for sqlalchemy
#It should get username, password, ip address, hostname, and database name in the URL info needed for connection.
# Template string to be the URL: 'postgressql://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

#we need to create an engine which connects us to postgres database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""
sessionmaker: This is a factory function provided by SQLAlchemy to create new Session objects. 
A Session is used to manage the persistence of objects and to perform operations on the database.

autocommit=False: This means that transactions are not automatically committed to the database. 
Instead, you will need to explicitly call commit() on the session to save changes. 
This provides more control over when changes are committed.

autoflush=False: This means that SQLAlchemy will not automatically flush pending changes to the database before each query.
Flushing is the process of synchronizing the session’s in-memory state with the database. 
Setting this to False can be useful to prevent unnecessary database operations, especially in scenarios 
where you want to manage flushing manually.

bind=engine: The bind parameter specifies the database engine to which the session should be connected. 
The engine is typically created using SQLAlchemy’s create_engine function and defines the database connection details.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""
-The Base class maintains metadata about all the models, which is used by SQLAlchemy to create tables and perform operations on them.
-declarative_base(): A function returns a new base class that you can use as the parent class for your model classes. 
This base class is not an instance but a class itself.
-Return Value: The declarative_base() function returns a new class (let’s call it Base), which is a base class for defining ORM models.
-Purpose: This Base class is used as a parent class for your ORM model classes. It provides the necessary infrastructure 
for SQLAlchemy to map the model classes to database tables.
-Usage: You create your model classes by inheriting from this Base class. 
Each model class then automatically has the behavior needed to interact with the database.
"""
Base = declarative_base()


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