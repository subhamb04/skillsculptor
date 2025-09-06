import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
from openai import OpenAI

load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

llm = AsyncOpenAI(
    base_url=base_url,
    api_key=google_api_key
)

chatllm = OpenAI(
    base_url=base_url,
    api_key=google_api_key
)

# Helper constant for model name
client = OpenAIChatCompletionsModel(
    openai_client=llm,
     model="gemini-2.5-flash" # Or another Gemini model like gemini-2.5-pro, gemini-1.5-flash etc.
)
