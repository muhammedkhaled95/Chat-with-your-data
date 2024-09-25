from pydantic_settings import BaseSettings

#Env variables using BaseSettings from Pydantic_settings
class Settings(BaseSettings):
    DATABASE: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    BASE_DIR: str
    class Config:
        env_file = ".env"

settings = Settings()

##############Documentation#######################
"""
The `Config` class inside the `Settings` class is a special nested class used by Pydantic's `BaseSettings` to configure settings-related behaviors. Here's a breakdown of what's happening:

1. **`Settings` Class**:
   - Inherits from `BaseSettings`, which is part of the `pydantic_settings` library.
   - Defines attributes that represent various configuration values, like database credentials and secret keys.

2. **`Config` Class**:
   - This is a nested class within the `Settings` class.
   - It is used to configure how Pydantic should handle loading and parsing environment variables for the `Settings` class.

3. **`env_file` Attribute**:
   - `env_file = ".env"` specifies that Pydantic should look for environment variables in a file named `.env` located in the same directory as your script.
   - Pydantic will automatically read this file and populate the attributes of the `Settings` class with the values defined in the `.env` file.

Here's a brief overview of the overall flow:

- **Initialization**:
  - When you create an instance of the `Settings` class (i.e., `settings = Settings()`), Pydantic reads the `.env` file as specified in the `Config` class.
  
- **Environment Variable Parsing**:
  - Pydantic parses the `.env` file and assigns values to the attributes of the `Settings` class (e.g., `DATABASE_HOST`, `DATABASE_PORT`, etc.) based on the keys and values found in the `.env` file.

This setup makes it easy to manage configuration settings and secrets in a clean and organized way, using environment variables stored in a `.env` file for better security and flexibility.
"""

"""
Alternative approach to load the .env file env variables:

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

This method provides a simple way to manage environment variables without the need for a Pydantic model, 
but you lose some of the validation and configuration features provided by Pydantic. 
If you need validation and structured access to your settings, Pydantic's BaseSettings can be very useful.
"""