import RAG_System as RAG
from fastapi import FastAPI
from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_query: str

app = FastAPI(title="Educational Assistant Service")


@app.get("/")
def root():
    return {"message": "RAG Education Assisstant API is running"}

@app.post("/query/")
def Query_Rag_System(request: QueryRequest):
    
    answer = RAG.RAG_Query(
        user_query=request.user_query
    )
    
    return {
        "answer": answer,
    }

