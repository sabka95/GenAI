import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


import json, os, time
import streamlit as st
from app.config import llm_call
from app.planner import choose_next
from app.orchestrator import JsonRpcProcess, MCPServer, Registry
from app.logging_utils import log_event

st.set_page_config(page_title="MCP Agentic App", layout="wide")
st.title("🔌 MCP Agentic Orchestrator")

# Load servers
import json as _json
cfg_path = os.getenv("SERVERS_CONFIG", "servers/servers.local.json")
servers_def = _json.load(open(cfg_path))

procs = {}
servers = {}
for s in servers_def["servers"]:
    p = JsonRpcProcess(s["name"], s["command"], s.get("args",[]), s.get("env",{}))
    procs[s["name"]] = p
    servers[s["name"]] = MCPServer(p)

reg = Registry(servers)

with st.sidebar:
    st.subheader("Connected tools")
    for key, meta in reg.index.items():
        st.write(f"**{key}** — {meta.get('description','(no description)')}")

user_goal = st.text_area("Enter your goal", placeholder="Find the latest data on X, load CSV Y, clean, and summarize…")
run = st.button("Run Plan")

if run and user_goal.strip():
    context = []
    for step in range(int(os.getenv("MAX_STEPS","8"))):
        plan = choose_next(user_goal, reg.index, "\n".join(context))
        log_event("plan", plan)
        if plan.get("action") == "respond":
            st.success(plan.get("text") or plan.get("rationale","Done."))
            break
        target = plan.get("target","")
        if ":" not in target:
            st.error(f"Bad target: {target}"); break
        sname, tname = target.split(":",1)
        args = plan.get("arguments",{})
        st.write(f"**Step {step+1}:** {sname}:{tname} → `{json.dumps(args)}`")
        try:
            result = servers[sname].call(tname, args)
            log_event("call", {"target":target, "args":args, "result":str(result)[:1000]})
            context.append(f"{target} => {json.dumps(result)[:1000]}")
            st.code(json.dumps(result, indent=2)[:4000])
        except Exception as e:
            log_event("error", {"target":target, "error":str(e)})
            st.warning(f"Call failed: {e}. Retrying or choosing alternative…")
            # simple fallback: ask the LLM to adapt
            context.append(f"ERROR calling {target}: {e}")
            continue
    else:
        st.info("Reached MAX_STEPS without terminal response.")
