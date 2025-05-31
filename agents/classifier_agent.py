# classifier_agent.py
import json
import uuid
from llm.langchain_llm import get_llm, prompt_model
from utils.logger import log_action

class ClassifierAgent:
    def __init__(self):
        self.llm = get_llm()

    def classify(self, raw_input: str, format_hint=None) -> dict:
        format_prompt = f"""
Detect the format of the following input:
Options: PDF, JSON, Email
Respond ONLY in this JSON format:
{{"format": "PDF/JSON/Email"}}

--- INPUT START ---
{raw_input[:1000]}
--- INPUT END ---
"""
        intent_prompt = f"""
You are an intelligent assistant. Classify the following input by its intent:
Options: Invoice, RFQ, Complaint, Regulation
Respond ONLY in this JSON format:
{{"intent": "Invoice/RFQ/Complaint/Regulation"}}

--- INPUT START ---
{raw_input[:1000]}
--- INPUT END ---
"""

        try:
            if not format_hint:
                format_response = prompt_model(self.llm, format_prompt)
                format_hint = json.loads(format_response).get("format", "Unknown")
                print(format_hint)  # Debugging line
            intent_response = prompt_model(self.llm, intent_prompt)
            intent_response = intent_response.strip('` \n')
            intent = json.loads(intent_response).get("intent", "Unknown")
            print(intent)  # Debugging line
            thread_id = f"{intent.lower()}-{uuid.uuid4().hex[:6]}"
            log_action(thread_id, "classification_done", f"Format: {format_hint}, Intent: {intent}")

            return {
                "format": format_hint.lower(),
                "intent": intent,
                "thread_id": thread_id
            }

        except Exception as e:
            thread_id = f"unknown-{uuid.uuid4().hex[:6]}"
            log_action(thread_id, "classification_failed", str(e))
            return {
                "format": "Unknown",
                "intent": "Unknown",
                "thread_id": thread_id,
                "error": str(e)
            }
