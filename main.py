from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.tutor_agent import TutorAgent
from dotenv import load_dotenv

# load env var
load_dotenv()

app = FastAPI(title="AI Tutor Multi-Agent System")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ini tutor agent
tutor = TutorAgent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    agent_used: str


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)


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