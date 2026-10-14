import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent_graph import build_agent_graph

compiled_graph = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global compiled_graph
    print("🔒 Initializing LangGraph Engine...")
    compiled_graph = build_agent_graph()
    yield

# ✅ Initialize FastAPI once with lifespan and CORS middleware
app = FastAPI(title="Security Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentQueryRequest(BaseModel):
    question: str = "What is the details for CVE-2024-1234?"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/agent/query")
async def query_agent(req: AgentQueryRequest):
    if not compiled_graph:
        raise HTTPException(status_code=503, detail="Graph engine not initialized")
    
    input_state = {"messages": [HumanMessage(content=req.question)]}
    final_state = await compiled_graph.ainvoke(input_state)
    
    last_message = final_state["messages"][-1]
    return {
        "response": last_message.content,
        "full_history": [f"[{m.__class__.__name__}]: {m.content}" for m in final_state["messages"]]
    }

if __name__ == "__main__":
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)