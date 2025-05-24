from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.tutor_agent import TutorAgent
from dotenv import load_dotenv
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Tutor Multi-Agent System")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize tutor agent
tutor = TutorAgent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    agent_used: str
    tools_used: List[str]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        result = await tutor.process_query(request.question)
        
        if not result:
            logger.warning(f"No answer found for question: {request.question}")
            raise HTTPException(status_code=404, detail="No answer found for the question.")
        
        logger.info(f"Question: {request.question}, Agent Used: {result['agent_used']}, Tools Used: {result['tools_used']}")
        
        return QueryResponse(
            answer=result["answer"],
            agent_used=result["agent_used"],
            tools_used=result["tools_used"]
        )
    except Exception as e:
        logger.error(f"Error processing question: {request.question}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)