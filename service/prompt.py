import yaml
from pathlib import Path
from core.loader import load_config_tools
from config.prompt import generate_llm_system_prompt

BASE_DIR = Path(__file__).resolve().parent.parent
TOOL_PATH = BASE_DIR / "config" / "tools.yaml"

# def build_tool_prompt_summary(tool_registry: dict) -> str:
#     summary_lines = []
#
#     for step in results:
#         tool = step['call']['tool']
#         function = step['call']['function']
#         result = step['result']
#
#         if tool == "market" and function == "get_symbol_kline_data":
#             data = result.get("data", {})
#             short = data.get("short_summary", {})
#             long = data.get("long_summary", {})
#
#             summary_lines.append("📈 Short-term:")
#             summary_lines.append(f"Buy Range: ${short.get('lowest_price')} ~ ${short.get('average_close')}")
#             summary_lines.append(f"Resistance: ${short.get('highest_price')}")
#
#             summary_lines.append("📊 Long-term:")
#             summary_lines.append(f"Buy Range: ${long.get('lowest_price')} ~ ${long.get('average_close')}")
#             summary_lines.append(f"Resistance: ${long.get('highest_price')}")
#
#         if tool == "market" and function == "get_symbol_fetch_news":
#             news_items = result if isinstance(result, list) else []
#             summary_lines.append("📰 Latest News Headlines:")
#             for news in news_items[:5]:
#                 summary_lines.append(f"- {news['title']} (Published at {news['published_at']})")
# 
#     return "\n".join(summary_lines)

def generate_final_system_prompt() -> str:
    registry = load_config_tools(TOOL_PATH)
    tool_desc = generate_llm_system_prompt(registry)
    return tool_desc


