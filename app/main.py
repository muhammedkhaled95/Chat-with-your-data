from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db import models
from app.api.v1.routers import auth, users, files, queries
from app.services.LLM_handling.llm_loader import load_llm
from contextlib import asynccontextmanager
import gc

#this line tells sqlalchemy to run the create statement to generate all of the tables in the beginning
#This line won't be needed if we are going to use Alembic for tables creation and architecture changes over time.
models.Base.metadata.create_all(bind=engine)

llm_model = None

# This is an instance of the FASTAPI class (which is our app which will be used to create all of our endpoints "APIs")
app = FastAPI()

# allowing all origins to talk to our API application (just for educational purposes but in reality, that's not secure)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"], #allowing only specific HTTP methods (like allowing only get request), use * means all is allowed.
    allow_headers=["*"],
)

app.include_router(auth.auth_router)
app.include_router(users.users_router)
app.include_router(files.files_router)
app.include_router(queries.queries_router)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This context manager handles the initialization and cleanup processes
    for the FastAPI application. It loads a Large Language Model (LLM) at 
    the startup of the application and makes it available throughout the 
    app's lifecycle. Additionally, it provides a place to include any 
    necessary cleanup code when the application shuts down.
    Args:
      app (FastAPI): The FastAPI application instance.
    Yields:
      None: Control is yielded back to the application after initialization.
    Initialization:
      - Loads the LLM model and assigns it to `app.state.llm_model`.
      - Prints a message indicating that the LLM model has been loaded.
    Cleanup:
      - Prints a message indicating that resources are being cleaned up.
      - (Optional) Add any additional cleanup code as needed.
    """
    global llm_model
    # Initialization: Load LLM model at app startup
    llm_model = load_llm(local=True)
    print("LLM model loaded")

    # Make the llm_model available throughout the app
    app.state.llm_model = llm_model

    # Yield control back to the app
    yield

    # Cleanup code can go here if needed (e.g., closing connections)
    print("Cleaning up resources")
    
    if llm_model:
        print("Unloading the LLM...")
        del llm_model  # Dereference the LLM
        gc.collect()  # Force garbage collection to free memory
        print("LLM unloaded successfully")


# Use lifespan in the app
app.router.lifespan_context = lifespan

        
"""
- @app.get("/"): This is a decorator provided by FastAPI that indicates that the function below will handle HTTP GET requests 
  to the root path ("/").  In this case, the root path is the base URL of your application (e.g., http://localhost:8000/).
- This root endpoint can be used as a default endpoint in case no specific route was matched with the client request.
- Handler Functions: These are the functions or methods in your code that execute when a request matches a route. 
  They generate the response that gets sent back to the client.
- root() handler function is created which basically processes the client request of (GET) and returns the hard-coded JSON in it.
"""
@app.get("/")
async def root():
    return {"message": "Hello there."}