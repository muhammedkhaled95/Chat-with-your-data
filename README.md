# FastAPI-RAG-APP

## Overview

FastAPI-RAG-APP is a backend API project designed to enable users to interact with their own data through a chat interface. Each user can create an account, sign in, upload their own PDF files, and chat with the data contained within those files. This project leverages the Retrieval-Augmented Generation (RAG) technique by maintaining a separate vector store for each user. The LLM is loaded in memory when the app starts and the memory is freed when the app shuts down using the lifespan feature in Python.

## Features

- **User Authentication**: Users can create accounts and sign in to access their data.
- **PDF Upload**: Users can upload PDF files to the system.
- **Chat with Data**: Users can interact with the data in their uploaded PDFs through a chat interface.
- **RAG Technique**: Each user has a separate vector store to ensure personalized data retrieval.
- **Local LLM**: The project uses a local Large Language Model (LLM). [https://huggingface.co/TheBloke/CapybaraHermes-2.5-Mistral-7B-GGUF]
- **Local Embedding Model**: The embedding model is also hosted locally [sentence-transformers/all-MiniLM-L6-v2].

## Installation

To get started with FastAPI-RAG-APP, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/FastAPI-RAG-APP.git
    cd FastAPI-RAG-APP
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up PostgreSQL database:

    - Install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
    - Create a new database and user:

        ```sql
        CREATE DATABASE fastapi_rag_app;
        CREATE USER fastapi_user WITH PASSWORD 'yourpassword';
        GRANT ALL PRIVILEGES ON DATABASE fastapi_rag_app TO fastapi_user;
        ```

    - Update the database connection settings in your `config.py` or environment variables:

        ```python
        DATABASE_URL = "postgresql://fastapi_user:yourpassword@localhost/fastapi_rag_app"
        ```

4. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

## Usage

1. **Sign Up**: Create a new account.
2. **Sign In**: Log in to your account.
3. **Upload PDF**: Upload your PDF files.
4. **Chat**: Start chatting with the data in your uploaded PDFs.

## Contributing

This is an ongoing project, and contributions are welcomed! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.

## License

This project is open source and free to use under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [muhammedkhaled1110@gmail.com].
