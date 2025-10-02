import yaml
from pathlib import Path
from core.loader import load_config_tools
from config.prompt import generate_llm_system_prompt

BASE_DIR = Path(__file__).resolve().parent.parent
TOOL_PATH = BASE_DIR / "config" / "tools.yaml"

def generate_final_system_prompt() -> str:
    registry = load_config_tools(TOOL_PATH)
    tool_desc = generate_llm_system_prompt(registry)
    return tool_desc


