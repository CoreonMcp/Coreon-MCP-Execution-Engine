from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from dotenv import load_dotenv, set_key
from utils.common import get_resource_path
import os

ENV_PATH = get_resource_path(".env")

def ensure_openai_api_key() -> str:
    load_dotenv(dotenv_path=ENV_PATH, override=False)
    key = os.getenv("OPENAI_API_KEY", "").strip()

    if not key:
        print("🔐 Missing OpenAI API Key.")
        while True:
            key = input(" > ").strip()
            if key.startswith("sk-"):
                set_key(str(ENV_PATH), "OPENAI_API_KEY", key)
                print("✅ OPENAI_API_KEY has been saved.")
                break
            else:
                print("❗️Format error. It must start with sk-. Please re-enter:")

    load_dotenv(dotenv_path=ENV_PATH, override=True)
def create_app():
    ensure_openai_api_key()

    app = FastAPI(
        title="MCP Execution Engine API",
        description="MCP Server API for developers",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    return app

app = create_app()

