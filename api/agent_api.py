from fastapi import APIRouter, Request
from agent.phoenix_agent import PhoenixAgent

router = APIRouter()
agent = PhoenixAgent()

@router.post(\"/agent/ask\")
async def ask_agent(request: Request):
    data = await request.json()
    query = data.get(\"query\", \"\")
    return {"response": agent.process(query)}