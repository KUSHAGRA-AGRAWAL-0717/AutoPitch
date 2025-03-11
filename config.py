import os

# Define API Key and Model Name directly
GROQ_API_KEY = "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"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"

# Define USER_AGENT directly
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

# Ensure USER_AGENT is always available
if not USER_AGENT:
    print("⚠️ Warning: USER_AGENT not set. Using default.")
    USER_AGENT = "Mozilla/5.0"
