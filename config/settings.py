import os
from dotenv import load_dotenv
from pathlib import Path

class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = ""
        self.WALLET_PRIVATE_KEY = ""
        self.WALLET_ADDRESS = ""
        self.MCP_LANG = ""
        self.MODEL_NAME = ""
        self.REDIS_URL = ""
        self.ENV = ""
        self.LOG_LEVEL = ""
        self.PROXY_BASE_URL = ""
        self.TG_API_URL = ""
        self.reload()

    def reload(self):
        env_path = Path(__file__).resolve().parent.parent / ".env"
        load_dotenv(dotenv_path=env_path, override=True)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip().strip("'\"")
        self.WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY", "").strip().strip("'\"")
        self.WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "").strip().strip("'\"")
        self.MCP_LANG = os.getenv("MCP_LANG", "en").strip().lower().strip("'\"")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
        self.TG_API_URL = "https://api.telegram.org/bot"
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.ENV = os.getenv("ENV", "DEV")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")
        self.PROXY_BASE_URL = os.getenv("PROXY_BASE_URL", "https://api.coreon.pro")
        self.WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "")

settings = Settings()