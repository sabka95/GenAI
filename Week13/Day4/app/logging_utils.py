import json, os, time
from rich.console import Console

console = Console()
LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")

def log_event(kind: str, payload):
    console.log({"kind": kind, "at": time.time(), "payload": payload})
