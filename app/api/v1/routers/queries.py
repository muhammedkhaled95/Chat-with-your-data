from fastapi import APIRouter, Depends, HTTPException, status
import app
import os
from app.core.config import settings
from app.db import schemas
from app.services.LLM_handling import querying
from sqlalchemy.orm import Session
from app.api.v1.dependencies.deps import get_db, get_current_user

queries_router = APIRouter(prefix="", tags=["Queries"],)

@queries_router.get("/query", response_model=schemas.LLMAnswer)
async def answer_user_query(query: schemas.UserQuery,
                            db: Session = Depends(get_db),
                            current_user: schemas.User = Depends(get_current_user)):
    user_folder: str = settings.BASE_DIR + "\\" + current_user.user_folder_name
    db_faiss_path_for_current_user = user_folder + "\\vector_store\\db_faiss"
    print(f"db_faiss_path_for_current_user = {db_faiss_path_for_current_user}")
    # This is called lazy import to avoid circular import issue between this file "queries.py" and "main.py"
    from app.main import llm_model
    print(f"llm_model = {llm_model}")
    qa_result = querying.qa_bot(db_faiss_path_for_current_user, llm_model)
    answer = qa_result.run(query.query)  
    print(f"answer = {answer}")
    return {"answer": answer}