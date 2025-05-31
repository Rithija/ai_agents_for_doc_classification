# Multi-Agent AI Document Classifier & Processor

🚀 **Smart Document Triage with PDF, JSON, Email Routing**
📁 Built with Python, LangChain (LLM), Redis, and Streamlit

---

## 🔍 Overview

This project is a **multi-agent AI system** that accepts documents in various formats (**PDF, Email, JSON**) and intelligently:

* Classifies the **document format** and **business intent** (Invoice, RFQ, Complaint, Regulation)
* Routes the input to the correct **processing agent** (EmailAgent, JSONAgent, PDFAgent)
* Extracts structured data (e.g., sender info, invoice fields, anomalies)
* Stores traceable output in **Redis-based shared memory** for chain-of-processing transparency

> This project leverages **LLMs**, **LangChain**, and **agent orchestration** for real-world intelligent document workflows.

---

## 🧠 Key Features

| Feature                     | Description                                                         |
| --------------------------- | ------------------------------------------------------------------- |
| 📤 Format Detection         | Automatically detects if input is PDF, JSON, or Email               |
| 🧾 Intent Classification    | Understands if the doc is an Invoice, RFQ, Complaint, or Regulation |
| 🧠 LLM-Powered Extraction   | Uses LLMs to extract and clean structured fields from natural text  |
| 🔁 Multi-Agent Routing      | Orchestrates document to the right processing agent                 |
| 🧩 Shared Memory via Redis  | Persists extracted fields, metadata, thread ID for traceability     |
| 📊 Anomaly Detection (JSON) | Flags missing/suspicious fields in structured JSON                  |
| 📨 CRM Formatting (Email)   | Extracts sender info + urgency for downstream CRM integration       |
| 📄 Streamlit UI             | Upload interface with live logs, previews, and Redis-stored results |

---

## 📁 Folder Structure

```bash
.
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   ├── json_agent.py
│   └── pdf_agent.py
├── router/orchestrator.py
├── memory/redis_memory.py
├── utils/
│   ├── logger.py
│   ├── json_cleaner.py
│   └── file_handler.py
├── llm/langchain_llm.py
├── app.py  # Streamlit UI
├── requirements.txt
└── README.md
```

---

## 🖼️ Sample Output Screenshots
![email_input](/outputs/Screenshot%202025-05-31%20233205.png)
![json_input](/outputs/Screenshot%202025-05-31%20233237.png)
![json_input](/outputs/Screenshot%202025-05-31%20233301.png)
![pdf_input](/outputs/Screenshot%202025-05-31%20233319.png)
![pdf_input](/outputs/Screenshot%202025-05-31%20233331.png)


---

## 📦 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourname/multi-agent-ai-docs.git
cd multi-agent-ai-docs
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure Environment**
   Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

4. **Run the Streamlit App**

```bash
streamlit run app.py
```

---

## 🛠️ Requirements

```
langchain
langchain-groq
redis
streamlit
python-dotenv
pdfplumber  # for PDF extraction
```

---

## 🌐 Project Highlights

* Real-time classification using **LLMs** (via LangChain)
* Seamless orchestration across multi-modal document types
* Context-sharing using **Redis-based memory architecture**
* Fully interactive UI with **Streamlit**
* Highly modular structure for extensibility to other formats or intents


---

Thank you for checking out this project 🙌
