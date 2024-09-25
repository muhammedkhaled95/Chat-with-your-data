from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from app.db import schemas, crud
from app.api.v1.dependencies.deps import get_current_user, get_db
from typing import List, Annotated
from sqlalchemy.orm import Session
import mimetypes
from app.core.config import settings
from app.services.LLM_handling.embedding import create_vector_db

files_router = APIRouter(prefix="", tags=["files"])


@files_router.post("/upload/{user_id}/")
async def upload_file(user_id: str, 
                      file: UploadFile,
                      db: Session = Depends(get_db),
                      current_user: schemas.User = Depends(get_current_user)):
    print(file.filename)
    print(f"current_user_id = {current_user.id}")
    print(f"user_id = {user_id}")
    if int(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to upload files for this user.")

    print(settings.BASE_DIR)
    user_folder: str = settings.BASE_DIR + "\\" + current_user.user_folder_name
    print(f"user_folder = {user_folder}")
    # Define the path where the file will be saved
    file_path: Path = Path(user_folder + "\\" + file.filename)
    print(f"file_path = {file_path}")
    # Save the file to the user folder
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        # Determine the file type
        file_type, _ = mimetypes.guess_type(file.filename)

        # Create the file schema object
        file_create = schemas.FileCreate(filename=file.filename, file_type=file_type, file_path=str(file_path))

        # Save the file information to the database
        await crud.create_file(db, file_create, int(user_id))
        file.file.close()  # Close the file object to release resources


        # Create the vector database
        await create_vector_db(user_folder, user_folder + "\\vector_store\\db_faiss")
        
    return JSONResponse(content={"message": f"File '{file.filename}' uploaded successfully to user {user_id}."})


@files_router.get("/files/{user_id}/", response_model=List[schemas.File])
async def list_user_files(user_id: str,
                          current_user: schemas.User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to view files for this user.")
    
    # Define the path for the user's folder
    user_folder = Path(settings.BASE_DIR) / user_id

    # Check if the user folder exists
    if not user_folder.exists():
        raise HTTPException(status_code=404, detail=f"User folder for {user_id} not found.")
    
    # List all files in the user folder
    files = [file.name for file in user_folder.iterdir() if file.is_file()]

    return {"user_id": user_id, "files": files}