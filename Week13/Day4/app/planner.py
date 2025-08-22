from typing import Dict, Any, List
from app.config import llm_call

SYSTEM = (
    "You are a helpful planner. Given a user goal and a catalog of MCP tools, "
    "choose the next best tool call (server:tool, arguments as JSON). "
    "Only pick tools that plausibly advance the goal. If no tool fits, return 'respond' with a short answer. "
    "Prefer: web/search → files/CSV → custom tool."
)

PROMPT = (
    "Goal: {goal}\n\n"
    "Available tools (server:tool → description):\n{catalog}\n\n"
    "Context so far: {context}\n\n"
    "Return JSON with keys: action ('call'|'respond'), target (e.g. 'web:search'), arguments (object), and rationale."
)

def choose_next(goal: str, catalog: Dict[str,Dict[str,Any]], context: str) -> Dict[str, Any]:
    cat_text = "\n".join([f"- {k} → {v.get('description','')}" for k,v in catalog.items()])
    text = PROMPT.format(goal=goal, catalog=cat_text, context=context)
    out = llm_call(SYSTEM, text)

    return out
