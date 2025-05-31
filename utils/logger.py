# utils/logger.py
import json
from datetime import datetime
from redis import Redis

redis = Redis(host="localhost", port=6379, decode_responses=True)

def log_action(thread_id: str, action_type: str, message: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action_type,
        "message": message
    }
    redis.rpush(f"log:{thread_id}", json.dumps(log_entry))

def get_logs(thread_id: str):
    logs = redis.lrange(f"log:{thread_id}", 0, -1)
    return [json.loads(entry) for entry in logs]
