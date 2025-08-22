import json, subprocess, threading, queue, uuid, time
from typing import Any, Dict, List

Json = Dict[str, Any]
MCP_PROTOCOL_VERSION = "2025-06-18"  # string arbitraire ok

class JsonRpcProcess:
    def __init__(self, name: str, command: str, args: List[str] = None, env: Dict[str,str] = None):
        self.name = name
        self.proc = subprocess.Popen(
            [command] + (args or []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env={**(env or {})} or None
        )
        self._out_q: "queue.Queue[str]" = queue.Queue()
        self._reader = threading.Thread(target=self._read_stdout, daemon=True); self._reader.start()

        self._err_reader = threading.Thread(target=self._read_stderr, daemon=True); self._err_reader.start()

        # Handshake (best effort): initialize -> initialized (notification)
        self._initialized = False
        try:
            self._initialize()
            self._initialized = True
        except Exception as e:
            print(f"[{self.name}] initialize failed: {e} (will try without initialize)")

    def _read_stdout(self):
        for line in self.proc.stdout:
            if line.strip():
                self._out_q.put(line)

    def _read_stderr(self):
        for line in self.proc.stderr:
            print(f"[{self.name} STDERR] {line.rstrip()}")

    def request(self, method: str, params: Json) -> Json:
        rid = str(uuid.uuid4())
        req = {"jsonrpc": "2.0", "id": rid, "method": method, "params": params}
        if not self.proc or not self.proc.stdin:
            raise RuntimeError(f"{self.name}: process not started")
        self.proc.stdin.write(json.dumps(req) + "\n"); self.proc.stdin.flush()
        while True:
            line = self._out_q.get(timeout=60)
            msg = json.loads(line)
            if msg.get("id") == rid:
                if "error" in msg:
                    raise RuntimeError(f"{self.name} {method} error: {msg['error']}")
                return msg.get("result", {})

    def notify(self, method: str, params: Json):
        # JSON-RPC notification (sans id)
        note = {"jsonrpc": "2.0", "method": method, "params": params}
        self.proc.stdin.write(json.dumps(note) + "\n"); self.proc.stdin.flush()

    def _initialize(self):
        params = {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {"tools": {"list": True, "call": True}},
            "clientInfo": {"name": "mcp-mini-orchestrator", "version": "0.1.0"},
        }
        # 1) initialize (attend une réponse)
        self.request("initialize", params)
        # 2) initialized (notification) – plusieurs serveurs l'attendent
        self.notify("initialized", {})
        # 3) petite pause pour éviter "request before initialization complete"
        time.sleep(0.1)

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass


class MCPServer:
    def __init__(self, proc: JsonRpcProcess):
        self.proc = proc

    def list_tools(self) -> List[Json]:
        # Si initialize a échoué (serveur très simple), essaye quand même tools/list
        res = self.proc.request("tools/list", {})
        tools = res.get("tools") if isinstance(res, dict) else None
        return tools or []

    def call(self, tool: str, arguments: Json) -> Json:
        return self.proc.request("tools/call", {"name": tool, "arguments": arguments})


class Registry:
    def __init__(self, servers: Dict[str, MCPServer]):
        self.servers = servers
        self.index: Dict[str, Dict] = {}
        for sname, srv in servers.items():
            try:
                for t in srv.list_tools():
                    key = f"{sname}:{t.get('name','unknown')}"
                    self.index[key] = {**t, "server": sname}
            except Exception as e:
                print(f"[WARN] unable to list tools for {sname}: {e}")

    def find(self, query: str) -> List[str]:
        q = query.lower()
        return [k for k,v in self.index.items() if q in k.lower() or q in json.dumps(v).lower()]
