import os, json, httpx
from dotenv import load_dotenv
load_dotenv()

LLM_BACKEND = os.getenv("LLM_BACKEND", "groq")

class LLM:
    def __init__(self):
        self.backend = LLM_BACKEND
        if self.backend == "groq":
            self.base = os.getenv("GROQ_BASE_URL")
            self.key = os.getenv("GROQ_API_KEY")
            self.model = os.getenv("GROQ_MODEL")
        else:
            self.base = os.getenv("OLLAMA_BASE_URL")
            self.model = os.getenv("OLLAMA_MODEL")

    def __call_me(self, system: str, user: str):
        if self.backend == "groq":
            url = f"{self.base}/chat/completions"
            headers = {"Authorization": f"Bearer {self.key}"}
            # Pas de response_format -> évite le 400
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
                "temperature": 0.2
            }
            with httpx.Client(timeout=60) as c:
                r = c.post(url, headers=headers, json=payload)
                try:
                    r.raise_for_status()
                except httpx.HTTPStatusError:
                    # remonter un message lisible dans Streamlit
                    raise RuntimeError(f"Groq HTTP {r.status_code}: {r.text}")
                j = r.json()
            return j["choices"][0]["message"]["content"]

        else:  # ollama
            url = f"{self.base}/api/chat"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
                "format": "json"
            }
            with httpx.Client(timeout=60) as c:
                r = c.post(url, json=payload); r.raise_for_status(); j = r.json()
            return j["message"]["content"]

LLM_INSTANCE = LLM()

def llm_call(system: str, user: str):
    txt = LLM_INSTANCE._LLM__call_me(system, user)
    try:
        return json.loads(txt)  # on espère du JSON (le prompt du planner le demande)
    except Exception:
        return {
            "action": "respond",
            "target": None,
            "arguments": {},
            "rationale": "Failed to parse JSON; returning plain text.",
            "text": txt
        }
