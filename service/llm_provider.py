from openai import OpenAI

from config.settings import settings

def llm_generate_json(messages: list) -> str:
    settings.reload()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=800,
        timeout=60
    )
    return response.choices[0].message.content

