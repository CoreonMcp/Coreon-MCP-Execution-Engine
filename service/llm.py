import openai
import json

from config.settings import settings
from service.llm_provider import llm_generate_json
from typing import List, Dict

openai.api_key = settings.OPENAI_API_KEY

def parse_input_to_toolcalls(user_input: str, system_prompt:str) -> List[Dict]:
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        output_text = llm_generate_json(messages)

        return json.loads(output_text)

    except Exception as e:
        print("⚠️ The LLM response could not be interpreted as a valid ToolCall format:", e)
        return []

def generate_reply_from_results(prompt: str) -> List[Dict]:

    return llm_generate_json([{"role": "system", "content": prompt}])



