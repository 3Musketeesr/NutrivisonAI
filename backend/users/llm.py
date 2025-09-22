from langchain_google_genai import GoogleGenerativeAI
from backend.config import get_settings 


SETTINGS = get_settings() 
def get_llm():
    llm = GoogleGenerativeAI(model="gemini-2.5",google_api_key=SETTINGS.GOOGLE_API_KEY)
    return llm

