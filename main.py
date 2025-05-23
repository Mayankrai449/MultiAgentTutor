from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.tutor_agent import TutorAgent
import os
from dotenv import load_dotenv

# load env var
load_dotenv()

app = FastAPI(title="AI Tutor Multi-Agent System", version="1.0.0")

# ini tutor agent
tutor = TutorAgent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    agent_used: str


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        result = await tutor.process_query(request.question)
        return QueryResponse(
            answer=result["answer"],
            agent_used=result["agent_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)