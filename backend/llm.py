from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from backend.config import get_settings 


SETTINGS = get_settings() 
def get_llm():
    os.environ["GOOGLE_API_KEY"]= SETTINGS.GOOGLE_API_KEY  
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return llm

