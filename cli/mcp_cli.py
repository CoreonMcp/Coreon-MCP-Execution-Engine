import os
import asyncio
import yaml
import sys
from pathlib import Path
from dotenv import load_dotenv
from config.settings import settings
from utils.common import write_env_var, print_banner, print_welcome, get_resource_path
from utils.logging_utils import log_trace
from service.planner import MCPPlanner
from core.router import execute_toolcall_chain
from service.response import generate_final_reply
from core.loader import load_config_tools
import json

ENV_PATH = get_resource_path(".env")

REQUIRED_KEYS = [
    ("MCP_LANG", "🌐 Please select your tool language (EN / ZH), press Enter for default EN:", False),
    ("OPENAI_API_KEY", "🔐 Please enter your OpenAI API Key:", True),
    ("WALLET_ADDRESS", "🏦 (Optional) Enter wallet address, press Enter to skip.", False),
]

def init_env():
    load_dotenv(dotenv_path=ENV_PATH, override=False)

    if not ENV_PATH.exists():
        ENV_PATH.touch()

    updated = False
    pending_writes = {}

    try:
        for key, prompt_text, required in REQUIRED_KEYS:
            if not os.getenv(key):
                print(prompt_text)
                value = input(" > ").strip()

                if value.lower() == "exit":
                    print("👋 Exited the initialization process. No configuration has been saved.")
                    sys.exit(0)

                if key == "MCP_LANG" and not value:
                    value = "EN"

                if value:
                    pending_writes[key] = value
                    updated = True
                elif required:
                    print("❗️This field is required and cannot be skipped.\n")
                    return init_env()
    except KeyboardInterrupt:
        print("\n👋 Exited the initialization process. No configuration has been saved.")
        sys.exit(0)

    for key, value in pending_writes.items():
        write_env_var(key, value, ENV_PATH)

    if updated:
        print("✅ Config saved to .env")
        # print("📄 The current .env configuration is as follows:")
        # print(ENV_PATH.read_text())
    else:
        print("✅ Loaded existing config from .env")

    load_dotenv(dotenv_path=ENV_PATH, override=True)

async def main():
    log_trace("===== MCP EXECUTION SESSION START =====")
    print_banner()
    init_env()
    print_welcome()
    planner = MCPPlanner()
    tool_registry = load_config_tools()
    while True:
        try:
            user_input = input("\n🧠 Coreon MCP Execution Engine > ").strip()

            log_trace(f"USER INPUT:\n{user_input}")

            if user_input.lower() in ("exit", "quit"):
                print("👋 ！")
                break

            toolcalls = planner.plan(user_input)
            log_trace(f"PLANNER OUTPUT:\n{json.dumps(toolcalls, indent=2)}")

            results = await execute_toolcall_chain(toolcalls, registry=tool_registry)


            reply = generate_final_reply(user_input, results, lang=settings.MCP_LANG)
            log_trace(f"FORMATTER OUTPUT:\n{reply}")

            print("🤖", reply)
            log_trace("===== MCP EXECUTION SESSION END =====")
        except KeyboardInterrupt:
            log_trace("===== MCP EXECUTION SESSION END =====")
            break




