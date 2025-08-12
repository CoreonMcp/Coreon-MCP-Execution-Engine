from fastapi import APIRouter
from service.planner import MCPPlanner
from core.loader import load_config_tools
from core.router import execute_toolcall_chain
from service.response import generate_final_reply
from api.schema import AskPayload

router = APIRouter()
planner = MCPPlanner()
tool_registry = load_config_tools()

@router.post("/ask")
async def ask_agent(payload: AskPayload):
    toolcall = planner.plan(payload.question)
    results = await execute_toolcall_chain(toolcall, registry=tool_registry)
    reply = generate_final_reply(payload.question, results, lang=payload.lang)
    return {
        "success": True,
        "reply": reply
    }