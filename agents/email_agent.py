# agents/email_agent.py
import uuid
from datetime import datetime
from memory.redis_memory import SharedMemory
from llm.langchain_llm import get_llm, prompt_model
from utils.logger import log_action
import json
from utils.json_cleaner import extract_clean_json
class EmailAgent:
    def __init__(self):
        self.memory = SharedMemory()
        self.llm = get_llm()

    def process(self, email_text: str, intent="Unknown") -> str:
        thread_id = f"{intent.lower()}-{uuid.uuid4().hex[:6]}"
        timestamp = datetime.utcnow().isoformat()
        log_action(thread_id, "email_processing_started", "Extracting fields from email")

        try:
            prompt = f"""
Extract the following from this email:
- sender_name
- sender_email
- urgency (low/medium/high)
- message_summary (core content)

Respond ONLY in JSON format.

--- EMAIL START ---
{email_text}
--- EMAIL END ---
"""
            response = prompt_model(self.llm, prompt)
            print(f"LLM Response: {response}")  # Debugging line
            extracted = extract_clean_json(response)
            print(f"Extracted JSON: {extracted}")  # Debugging line

            result = {
                "source": "email",
                "type": "email",
                "intent": intent,
                "timestamp": timestamp,
                "values": extracted,
                "crm_format": {
                    "contact_name": extracted.get("sender_name"),
                    "contact_email": extracted.get("sender_email"),
                    "summary": extracted.get("message_summary"),
                    "priority": extracted.get("urgency"),
                },
                "thread_id": thread_id,
            }

            redis_key = self.memory.save(result)
            log_action(thread_id, "email_processing_success", f"Extracted fields: {list(extracted.keys())}")
            return thread_id, redis_key

        except Exception as e:
            redis_key = self.memory.save({
                "source": "email",
                "type": "email",
                "intent": intent,
                "timestamp": timestamp,
                "values": {},
                "error": str(e),
                "thread_id": thread_id
            })
            log_action(thread_id, "email_processing_failed", str(e))
            return thread_id, redis_key
