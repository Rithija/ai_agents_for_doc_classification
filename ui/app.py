# app.py
import sys
import os
import streamlit as st
import json
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from router.orchestrator import Orchestrator
from utils.file_handler import extract_text_from_pdf, extract_text_from_json, extract_text_from_email
from memory.redis_memory import SharedMemory
from utils.logger import get_logs

# UI Layout
st.set_page_config(page_title="Multi-Agent AI System", layout="wide")
st.title("📤 Multi-Agent AI Input Processor")

file = st.file_uploader("Upload a file (PDF, JSON, Email - .txt/.eml)", type=["pdf", "json", "txt", "eml"])

if file:
    # Infer format and extract raw text
    if file.type == "application/pdf":
        format_hint = "pdf"
        raw_text = extract_text_from_pdf(file)
    elif file.type == "application/json":
        format_hint = "json"
        raw_text = extract_text_from_json(file)
    else:
        format_hint = "email"
        raw_text = extract_text_from_email(file)

    st.subheader("📄 Raw Extracted Text")
    st.code(raw_text[:1000] + ("..." if len(raw_text) > 1000 else ""), language="text")

    # Trigger button
    if st.button("🚀 Run Classification & Routing"):
        orchestrator = Orchestrator()
        with st.spinner("Running agents..."):
            result = orchestrator.route(raw_text, format_hint)

        thread_id = result.get("thread_id")
        redis_key = result.get("redis_key")

        if result.get("success"):
            st.success(f"✅ Processed! Data stored under Redis key: `{redis_key}`")

            # Fetch and show stored data
            memory = SharedMemory()
            stored = memory.get(redis_key)
            st.subheader("🧠 Stored Data")
            try:
                st.json(stored)
            except:
                st.code(json.dumps(stored, indent=2), language="json")
        else:
            st.error("❌ Processing failed.")
            st.warning(result.get("error"))

        # Show logs
        if thread_id:
            st.subheader("🪵 Logs")
            logs = get_logs(thread_id)
            if logs:
                for entry in logs:
                    st.markdown(f"**[{entry['timestamp']}] {entry['action']}**: {entry['message']}")
            else:
                st.info("No logs found for this thread.")
