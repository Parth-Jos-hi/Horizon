from app.config import settings
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
MODEL = "llama-3.1-70b" 
def generate_text(prompt:str,system:str="",max_tokens:int = 512)->str:
    response = client.message.create(
        model = MODEL,
        max_tokens = max_tokens,
        system = system,
        messages = [{"role":"user","content":prompt}],
    )
    return "".join(block.text for block in response.content if block.type=="text")
