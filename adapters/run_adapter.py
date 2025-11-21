#!/usr/bin/env python3
import sys
import os
import time
from jsonrpc_adapter import create_app
import uvicorn


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp-only":
        backend_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:9981"

        os.execv(sys.executable, [sys.executable, "mcp_stdio_adapter.py", backend_url])
        return

    print("Starting Coreon MCP Server...", file=sys.stderr)

    app = create_app()

    def run_fastapi():
        uvicorn.run(app, host="127.0.0.1", port=9981, log_level="info")

    import threading
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    time.sleep(2)

    from mcp_stdio_adapter import main as adapter_main
    import asyncio
    asyncio.run(adapter_main())


if __name__ == "__main__":
    main()
