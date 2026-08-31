from fastapi import FastAPI
from pydantic import BaseModel, Field
from security.injection_detector import check_prompt
from security.logger import log_blocked_request, log_allowed_request
from llm.ollama_client import call_ollama

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)

@app.post("/chat")
def chat(req: ChatRequest):
    result = check_prompt(req.prompt)

    if result["blocked"]:
        log_blocked_request(req.prompt, result["score"], result["label"])
        return {
            "status": "blocked",
            "reason": "prompt_injection_detected",
            "label": result["label"],
            "score": result["score"]
        }

    log_allowed_request(req.prompt, result["score"])
    response = call_ollama(req.prompt)
    return {
        "status": "ok",
        "response": response,
        "security_check": result
    }

@app.get("/")
def health():
    return {"status": "NetShield gateway running"}