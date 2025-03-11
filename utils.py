import re

def clean_text(text):
    """Cleans extracted text by removing HTML, URLs, and special characters."""
    if not isinstance(text, str):
        return text  # Return unchanged if not a string
    
    text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9,.()\- ]', '', text)  # Remove special characters (keep punctuation)
    text = re.sub(r'\s{2,}', ' ', text).strip()  # Remove extra spaces
    return text
