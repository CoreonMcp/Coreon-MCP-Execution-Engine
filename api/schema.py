from pydantic import BaseModel, Field

class AskPayload(BaseModel):
    question: str = Field(..., description="The question user wants to ask")
    lang: str = Field("en", description="Language of response, default is 'en'")