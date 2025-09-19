#!/usr/bin/env python3
"""
主启动脚本 - 启动FastAPI后端和MCP适配器
"""
import sys
import os
import subprocess
import time
import signal
import atexit
from jsonrpc_adapter import create_app  # 导入您的FastAPI应用
import uvicorn


def main():
    # 如果有命令行参数 --mcp-only，只启动MCP适配器
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp-only":
        backend_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:9981"
        # 直接运行MCP适配器
        os.execv(sys.executable, [sys.executable, "mcp_stdio_adapter.py", backend_url])
        return

    print("Starting Coreon MCP Server...", file=sys.stderr)

    # 1. 启动FastAPI后端服务器
    app = create_app()

    # 在后台启动uvicorn
    def run_fastapi():
        uvicorn.run(app, host="127.0.0.1", port=9981, log_level="info")

    import threading
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # 等待FastAPI启动
    time.sleep(2)

    # 2. 启动MCP适配器（主进程）
    from mcp_stdio_adapter import main as adapter_main
    import asyncio
    asyncio.run(adapter_main())


if __name__ == "__main__":
    main()
