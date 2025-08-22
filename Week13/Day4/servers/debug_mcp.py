import json, subprocess

# Commande pour lancer ton serveur web
cmd = [
    r"D:\GENAI\Week13\Day4\Mini_Projet\.venv\Scripts\python.exe",
    "-m", "duckduckgo_mcp_server.server"
]

# Lance le process
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

# Envoie une requête tools/list
req = {"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
proc.stdin.write(json.dumps(req) + "\n")
proc.stdin.flush()

# Lis une réponse
resp = proc.stdout.readline()
print("Réponse du serveur:", resp)

proc.kill()
