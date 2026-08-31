import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/security_events.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_blocked_request(prompt: str, score: float, label: str):
    logging.warning(f"BLOCKED | score={score:.2f} | label={label} | prompt={prompt[:100]}")

def log_allowed_request(prompt: str, score: float):
    logging.info(f"ALLOWED | score={score:.2f} | prompt={prompt[:100]}")