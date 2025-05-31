# redis_memory.py
import redis
import json
from datetime import datetime
from config import REDIS_HOST, REDIS_PORT

class SharedMemory:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def save(self, data):
        data['timestamp'] = datetime.utcnow().isoformat()
        key = f"{data['type']}:{data['thread_id']}"
        self.client.set(key, json.dumps(data))
        return key

    def get(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None
