import sys, json, uuid

def write(msg):
    sys.stdout.write(json.dumps(msg) + "\n"); sys.stdout.flush()

TOOLS = [{
    "name":"insights.summarize",
    "description":"Summarize bullet points or short text into a brief.",
    "input_schema":{
        "type":"object",
        "properties":{
            "points":{"type":"array","items":{"type":"string"}},
            "bullet_points":{"type":"array","items":{"type":"string"}},
            "brief":{"type":"string"}
        },
        "additionalProperties": True
    }
}]

def summarize(args):
    pts = args.get("points") or args.get("bullet_points")
    brief = args.get("brief")
    if pts and isinstance(pts, list):
        txt = "; ".join([p.strip() for p in pts if isinstance(p, str) and p.strip()])
    elif isinstance(brief, str) and brief.strip():
        txt = brief.strip()
    else:
        return ""
    txt = txt.replace("\n"," ").strip()
    if len(txt) > 450: txt = txt[:450].rsplit(" ",1)[0] + "…"
    parts = [p.strip() for p in txt.split(";") if p.strip()]
    if len(parts) >= 2: return (parts[0] + ". " + parts[1])[:600]
    return txt[:600]

for line in sys.stdin:
    try:
        req = json.loads(line)
    except Exception:
        continue
    mid = req.get("id", str(uuid.uuid4()))
    m = req.get("method"); params = req.get("params", {}) or {}

    if m == "initialize":
        # Renvoie des capacités minimales
        write({"jsonrpc":"2.0","id":mid,"result":{
            "protocolVersion":"2025-06-18",
            "capabilities":{"tools":{"list":True,"call":True}},
            "serverInfo":{"name":"mine-toy","version":"0.1.0"}
        }})
    elif m == "tools/list":
        write({"jsonrpc":"2.0","id":mid,"result":{"tools": TOOLS}})
    elif m == "tools/call":
        name = params.get("name"); args = params.get("arguments",{}) or {}
        if name == "insights.summarize":
            out = summarize(args)
            write({"jsonrpc":"2.0","id":mid,"result":{"brief": out}})
        else:
            write({"jsonrpc":"2.0","id":mid,"error":{"code":-32601,"message":"Unknown tool"}})
    elif m == "initialized":
        # notification -> ignore poliment
        continue
    else:
        write({"jsonrpc":"2.0","id":mid,"error":{"code":-32601,"message":"Unknown method"}})
