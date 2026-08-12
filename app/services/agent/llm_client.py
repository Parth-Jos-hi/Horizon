from app.config import settings
from groq import Groq
client = Groq(api_key=settings.GROQ_API_KEY)
MODEL = "llama-3.1-70b"
def generate_text(prompt:str,system:str="",max_tokens:int = 512)->str:
    response = client.message.create(
        model = MODEL,
        max_tokens = max_tokens,
        system = system,
        messages = [{"role":"user","content":prompt}],
    )
    return "".join(block.text for block in response.content if block.type=="text")
