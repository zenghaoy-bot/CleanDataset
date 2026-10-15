from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")


llm_langchain = ChatOpenAI(
    model="qwen3.8-flash",
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
    timeout =60,
    extra_body={
        "enable_thinking": False
    }
)