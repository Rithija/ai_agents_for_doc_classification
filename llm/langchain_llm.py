from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def get_llm():
    return ChatGroq(groq_api_key=GROQ_API_KEY, model_name="meta-llama/llama-4-scout-17b-16e-instruct")

def prompt_model(llm, prompt):
    return str(llm.predict(prompt)).strip()
