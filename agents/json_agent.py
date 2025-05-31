# agents/json_agent.py
import uuid
import json
from datetime import datetime
from memory.redis_memory import SharedMemory
from llm.langchain_llm import get_llm, prompt_model
from utils.logger import log_action
from utils.json_cleaner import extract_clean_json
class JSONAgent:
    def __init__(self):
        self.memory = SharedMemory()
        self.llm = get_llm()

    def process(self, json_data: dict, intent="Unknown") -> str:
        thread_id = f"{intent.lower()}-{uuid.uuid4().hex[:6]}"
        timestamp = datetime.utcnow().isoformat()
        log_action(thread_id, "json_processing_started", "Started extracting fields from JSON")

        try:
            prompt = f"""
The user provided a JSON document related to "{intent}".
Extract relevant fields and detect any missing or suspicious values.

Respond in JSON format:
{{
  "extracted": {{...}},
  "anomalies": ["field1", "field2"]
}}

--- JSON INPUT ---
{json.dumps(json_data, indent=2)}
"""
            llm_response = prompt_model(self.llm, prompt)
            extracted = extract_clean_json(llm_response)
            print(f"LLM Response: {extracted}")  # Debugging line
            parsed = extracted

            result = {
                "source": "json",
                "type": "json",
                "intent": intent,
                "timestamp": timestamp,
                "values": parsed.get("extracted", {}),
                "anomalies": parsed.get("anomalies", []),
                "thread_id": thread_id,
            }

            redis_key = self.memory.save(result)
            log_action(thread_id, "json_processing_success", f"Extracted fields: {list(result['values'].keys())}")
            return thread_id, redis_key

        except Exception as e:
            redis_key = self.memory.save({
                "source": "json",
                "type": "json",
                "intent": intent,
                "timestamp": timestamp,
                "values": {},
                "error": str(e),
                "thread_id": thread_id
            })
            log_action(thread_id, "json_processing_failed", str(e))
            return thread_id, redis_key
