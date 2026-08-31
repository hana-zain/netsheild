from fastapi import FastAPI
from pydantic import BaseModel
from security.injection_detector import check_prompt
from llm.ollama_client import call_ollama

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(req: ChatRequest):
    result = check_prompt(req.prompt)

    if result["blocked"]:
        return {
            "status": "blocked",
            "reason": "prompt_injection_detected",
            "label": result["label"],
            "score": result["score"]
        }

    response = call_ollama(req.prompt)
    return {
        "status": "ok",
        "response": response,
        "security_check": result
    }

@app.get("/")
def health():
    return {"status": "NetShield gateway running"}