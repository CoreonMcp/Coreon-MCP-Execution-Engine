from pathlib import Path
from config.settings import settings
from langdetect import detect
import sys
import time


def print_banner():
    print(color_mcp_tag("=" * 60))
    w = color_mcp_tag("Welcome to \n")
    f = color_mcp_tag("Coreon MCP Execution Engine")
    print(f"🧠 {w}")

    print(color_mcp_tag(" ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗"))
    print(color_mcp_tag("██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║"))
    print(color_mcp_tag("██║     ██║   ██║██████╔╝█████╗  ██║   ██║██╔██╗ ██║"))
    print(color_mcp_tag("██║     ██║   ██║██╔══██╗██╔══╝  ██║   ██║██║╚██╗██║"))
    print(color_mcp_tag("╚██████╗╚██████╔╝██║  ██║███████╗╚██████╔╝██║ ╚████║"))
    print(color_mcp_tag(" ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝"))
    print(f"                    {f}")
    print(color_mcp_tag("=" * 60))

def print_welcome():
    settings.reload()
    if settings.MCP_LANG == "zh":
        print("\n📌 欢迎使用 MCP 终端助手，你可以尝试输入：")
        print(" - 我的钱包里有多少钱？")
        print(" - 0x 开头的 CA 地址现在值多少钱？")
        print(" - ... 这个币最近涨跌怎么样？")
        print(" - Elon Musk 有没有关注某个币？")
        print("💡 输入 'exit' 或按下 Ctrl+C 可退出程序\n")
    else:
        print("\n📌 Welcome to the MCP Terminal Assistant. Try typing:")
        print(" - How much is in my wallet?")
        print(" - How much is this CA worth? (e.g. 0x...)")
        print(" - What's the price trend of ...?")
        print(" - Has Elon Musk followed this project?")
        print("💡 Type 'exit' or press Ctrl+C to quit\n")


def write_env_var(key: str, value: str, path: Path):
    lines = []
    key_found = False

    if path.exists():
        with open(path, "r") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    key_found = True
                else:
                    lines.append(line)

    if not key_found:
        lines.append(f"{key}={value}\n")

    with open(path, "w") as f:
        f.writelines(lines)

def loading_animation(message="🤖 Loading...", duration=2.5, interval=0.5):
    steps = int(duration / interval)
    for i in range(steps):
        sys.stdout.write(f"\r{message}{'.' * (i % 4)}   ")
        sys.stdout.flush()
        time.sleep(interval)
    print("\r", end="")

def typewriter_print(text, delay=0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def color_mcp_tag(text="MCP") -> str:
    return f"\033[1;31m{text}\033[0m"

def find_project_root(marker=".env"):
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent
    raise FileNotFoundError(f"Cannot find project root with {marker} file.")


def get_resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):

        return Path(sys._MEIPASS) / relative_path

    return Path(relative_path)

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"

def extract_step_recent_data(result_list, tool_call, key_name):
    for item in result_list:
        call = item.get("call", {})
        if call.get("tool") == tool_call:
            data = item.get("result", {}).get("data", {})
            return data.get(key_name, [])
    return []