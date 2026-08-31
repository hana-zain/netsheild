from transformers import pipeline

MODEL_NAME = "protectai/deberta-v3-base-prompt-injection-v2"

classifier = pipeline(
    "text-classification",
    model=MODEL_NAME,
    truncation=True,
    max_length=512,
)

def check_prompt(text: str, threshold: float = 0.85) -> dict:
    result = classifier(text)[0]   # {'label': 'INJECTION' or 'SAFE', 'score': 0.93}
    is_blocked = result["label"] == "INJECTION" and result["score"] >= threshold
    return {
        "blocked": is_blocked,
        "label": result["label"],
        "score": result["score"]
    }