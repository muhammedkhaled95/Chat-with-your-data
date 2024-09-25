# Chat With Your Data

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
    git clone https://github.com/muhammedkhaled95/Chat-with-your-data.git
    cd Chat with your data
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up PostgreSQL database:

    - Install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
    - Create a new database and user:

        ```sql
        CREATE DATABASE chat_with_your_data_app;
        CREATE USER fastapi_user WITH PASSWORD 'yourpassword';
        GRANT ALL PRIVILEGES ON DATABASE fastapi_rag_app TO fastapi_user;
        ```

    - Update the database connection settings in your `config.py` or environment variables:

        ```python
        DATABASE_URL = "postgresql://fastapi_user:yourpassword@localhost/chat_with_your_data_app"
        ```

4. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

## Testing

### To test the APIs, you can use tools like Postman or Thunder Client in VSCode

#### Using Postman

1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/).
2. Open Postman and create a new request.
3. Set the request method (GET, POST, etc.) and enter the API endpoint URL.
4. Add any necessary headers, parameters, or body content.
5. Click "Send" to execute the request and view the response.

#### Using Thunder Client in VSCode

1. Install the Thunder Client extension from the VSCode marketplace.
2. Open the Thunder Client panel in VSCode.
3. Create a new request by setting the method and entering the API endpoint URL.
4. Add any necessary headers, parameters, or body content.
5. Click "Send" to execute the request and view the response.

    Both tools allow you to save your requests and organize them into collections for easy access and reuse.

## Usage

1. **Sign Up**: Create a new account.
2. **Sign In**: Log in to your account.
3. **Upload PDF**: Upload your PDF files.
4. **Chat**: Start chatting with the data in your uploaded PDFs.

## Contributing

This is an ongoing project, and contributions are welcomed! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request. Here is a step-by-step guide on how you can contribute:

1. **Fork the Repository**: Click the "Fork" button at the top right corner of the repository page to create a copy of the repository on your GitHub account.

2. **Clone the Forked Repository**: Clone the forked repository to your local machine using the following command:

    ```bash
    git clone https://github.com/your-username/Chat-with-your-data.git
    cd Chat-with-your-data
    ```

3. **Create a New Branch**: Create a new branch for your feature or bug fix. Use a descriptive name for your branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes**: Implement your feature or fix the bug in your local repository.

5. **Commit Your Changes**: Commit your changes with a descriptive commit message:

    ```bash
    git add .
    git commit -m "Description of the feature or fix"
    ```

6. **Push to Your Fork**: Push your changes to your forked repository:

    ```bash
    git push origin feature/your-feature-name
    ```

7. **Open a Pull Request**: Go to the original repository on GitHub and open a pull request. Provide a clear description of your changes and any related issue numbers.

8. **Review Process**: Your pull request will be reviewed by the repository maintainers. Be prepared to make any necessary changes based on feedback.

9. **Merge**: Once your pull request is approved, it will be merged into the main branch.

Thank you for your contributions!

## License

This project is open source and free to use under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [muhammedkhaled1110@gmail.com].
