# agents/pdf_agent.py
import uuid
from datetime import datetime
from memory.redis_memory import SharedMemory
from llm.langchain_llm import get_llm, prompt_model
from utils.logger import log_action
import json
from utils.json_cleaner import extract_clean_json

class PDFAgent:
    def __init__(self):
        self.memory = SharedMemory()
        self.llm = get_llm()

    def process(self, text: str, intent="Unknown") -> str:
        thread_id = f"{intent.lower()}-{uuid.uuid4().hex[:6]}"
        timestamp = datetime.utcnow().isoformat()
        log_action(thread_id, "pdf_processing_started", "Started PDF text analysis")

        try:
            prompt = f"""
Extract structured information from the following PDF-extracted text related to "{intent}".

Return fields such as:
- document_title
- reference_number
- involved_parties
- key_dates (issue_date, due_date, etc.)
- total_amount (if invoice)
- summary

Respond ONLY in JSON format with appropriate keys.

--- PDF TEXT START ---
{text}
--- PDF TEXT END ---
"""
            response = prompt_model(self.llm, prompt).strip('` \n')
            extracted = extract_clean_json(response)
            print(f"LLM Response: {extracted}")  # Debugging line   
            parsed = extracted

            result = {
                "source": "pdf",
                "type": "pdf",
                "intent": intent,
                "timestamp": timestamp,
                "values": parsed,
                "thread_id": thread_id,
            }

            redis_key = self.memory.save(result)
            log_action(thread_id, "pdf_processing_success", f"Extracted fields: {list(parsed.keys())}")
            return thread_id, redis_key

        except Exception as e:
            redis_key = self.memory.save({
                "source": "pdf",
                "type": "pdf",
                "intent": intent,
                "timestamp": timestamp,
                "values": {},
                "error": str(e),
                "thread_id": thread_id
            })
            log_action(thread_id, "pdf_processing_failed", str(e))
            return thread_id, redis_key
