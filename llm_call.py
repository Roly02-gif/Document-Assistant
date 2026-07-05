import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_response(query: str) -> str:

  client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=os.getenv("OPENROUTER_API_KEY"),
  )

  try:
    response = client.responses.create(
        model="openai/gpt-oss-120b:free",
        input=query,
    )
    response = response.output_text
    return response if response else ValueError("The LLM response did not contain any text")

  except Exception as e:
    raise RuntimeError(f"Error calling LLM: {e}") from e
