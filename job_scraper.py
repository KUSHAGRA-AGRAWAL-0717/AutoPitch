import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import GROQ_API_KEY, LLM_MODEL_NAME, USER_AGENT  # Import USER_AGENT
from utils import clean_text

# Load LLM model
llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name=LLM_MODEL_NAME)

def extract_job_details(url):
    """Extracts job details from the given URL and cleans the data."""
    
    try:
        # Create a requests session with User-Agent header
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

        # Fetch page content manually
        response = session.get(url)
        response.raise_for_status()  # Raise error for bad responses
        page_data = response.text[:10000]  # Limit to 10,000 characters

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            Extract job details in JSON format with `role`, `company`, `location`, `experience`, `skills`, `responsibilities`, `description`.
            Return only JSON output.
            """
        )

        chain_extract = prompt_extract | llm
        result = chain_extract.invoke(input={'page_data': page_data})

        json_parser = JsonOutputParser()
        job_details = json_parser.parse(result.content)

        if isinstance(job_details, list):
            job_details = job_details[0]

        # Clean the extracted job details
        cleaned_job_details = {key: clean_text(value) if isinstance(value, str) else value for key, value in job_details.items()}
        
        return cleaned_job_details

    except requests.exceptions.RequestException as req_err:
        print(f"❌ Network error: {req_err}")
    except Exception as e:
        print(f"❌ Error extracting job details: {e}")
    
    return None
