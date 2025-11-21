import sys
import asyncio
from utils.common import print_banner
from cli.mcp_cli import main
def print_usage():
    print("🛠 Usage:")
    print("   docker run --rm -it coreonmcp/coreon-mcp-execution-engine start cli")
    print("   docker run --rm -it  -p [ip:ip] coreonmcp/coreon-mcp-execution-engine start server")
    print("   docker run --rm -it coreonmcp/coreon-mcp-execution-engine start Telegram-bot")

def start_cli():
    try:
        print("🤖 Start MCP Cli")
        from cli.mcp_cli import main
        asyncio.run(main())
    except ImportError:
        print("❌ Failed to start CLI: cli.mcp_cli not found.")
    except KeyboardInterrupt:
        print("\n👋 Exit MCP CLI by user (Ctrl+C)")

def start_server():
    try:
        print("🤖 Start MCP Server")
        from server.mcp_server import app
        import uvicorn
        print_banner()
        uvicorn.run(app, host="0.0.0.0", port=8181, reload=False)
    except ImportError:
        print("❌ Failed to start Server: server.mcp_server not found.")
    except KeyboardInterrupt:
        print("\n👋 Exit MCP Server by user (Ctrl+C)")

def start_telegram_bot():
    try:
        print("🤖 Start Telegram Bot...")
        from bot.telegram_bot import start_bot
        asyncio.run(start_bot())
    except ImportError:
        print("❌ Failed to start Telegram Bot: bot.telegram_bot not found.")
    except KeyboardInterrupt:
        print("\n👋 Exit Telegram Bot by user (Ctrl+C)")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "start":
        mode = sys.argv[2].lower()
        if mode == "cli":
            start_cli()
        elif mode == "server":
            start_server()
        elif mode == "telegram-bot":
            start_telegram_bot()
        else:
            print("❗ Unknown mode:", mode)
            print_usage()
    else:
        print("❗ Invalid arguments")
        print_usage()