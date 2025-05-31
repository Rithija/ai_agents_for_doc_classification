# orchestrator.py
from agents.email_agent import EmailAgent
from agents.json_agent import JSONAgent
from agents.pdf_agent import PDFAgent
from agents.classifier_agent import ClassifierAgent
from utils.logger import log_action

class Orchestrator:
    def __init__(self):
        self.classifier = ClassifierAgent()
        self.email_agent = EmailAgent()
        self.json_agent = JSONAgent()
        self.pdf_agent = PDFAgent()

    def route(self, raw_input, format_hint=None):
        classification = self.classifier.classify(raw_input, format_hint)
        format_ = classification.get("format", "").lower()
        intent = classification.get("intent", "Unknown")
        thread_id = classification.get("thread_id")

        log_action(thread_id, "routing_started", f"Routing to agent for format: {format_}")

        try:
            if format_ == "json":
                import json
                parsed_input = json.loads(raw_input)
                thread_id, redis_key = self.json_agent.process(parsed_input, intent)
            elif format_ == "email":
                thread_id, redis_key = self.email_agent.process(raw_input, intent)
            elif format_ == "pdf":
                thread_id, redis_key = self.pdf_agent.process(raw_input, intent)
            else:
                log_action(thread_id, "routing_failed", f"Unknown format: {format_}")
                return {"error": f"Unknown format: {format_}", "thread_id": thread_id, "redis_key": f"unknown:{thread_id}"}

            redis_key = f"{format_}:{thread_id}"
            log_action(thread_id, "routing_success", f"Routed and processed successfully")
            return {"success": True, "thread_id": thread_id, "redis_key": redis_key}

        except Exception as e:
            log_action(thread_id, "processing_failed", str(e))
            return {"success": False, "error": str(e), "thread_id": thread_id, "redis_key": f"{format_}:{thread_id}"}
