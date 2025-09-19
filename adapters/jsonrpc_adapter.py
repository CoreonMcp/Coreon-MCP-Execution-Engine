from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import uuid
import sys
import os

MCP_SERVER_URL = "http://localhost:9000"


class JsonRpcRequest(BaseModel):
    jsonrpc: str
    method: str
    params: dict | None = None
    id: str | int | None = None


def create_app() -> FastAPI:
    app = FastAPI(title="MCP JSON-RPC Adapter", version="1.0.0")

    @app.on_event("startup")
    async def startup_event():
        """启动时记录信息"""
        print(f"[PID:{os.getpid()}] FastAPI adapter started", file=sys.stderr)
        print(f"[PID:{os.getpid()}] Backend URL: {MCP_SERVER_URL}", file=sys.stderr)

    @app.get("/health")
    async def health_check():
        """健康检查端点"""
        return {
            "status": "healthy",
            "pid": os.getpid(),
            "backend_url": MCP_SERVER_URL
        }

    @app.get("/")
    async def root():
        """根路径"""
        return {
            "message": "Coreon MCP JSON-RPC Adapter",
            "version": "1.0.0",
            "pid": os.getpid()
        }

    @app.post("/jsonrpc")
    async def handle_request(req: JsonRpcRequest, request: Request):
        rpc_id = req.id or str(uuid.uuid4())

        print(f"[PID:{os.getpid()}] Received request: {req.method}", file=sys.stderr)

        try:
            if req.method == "get_balance":
                wallet = req.params.get("wallet") if req.params else None
                if not wallet:
                    return {
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {"code": -32602, "message": "Missing wallet parameter"}
                    }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(f"{MCP_SERVER_URL}/token/balance", json={"wallet": wallet})
                data = resp.json()
                result = {"balance": data.get("balance")}

            elif req.method == "get_wallet_address":
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(f"{MCP_SERVER_URL}/token/address")
                data = resp.json()
                result = {"wallet_address": data.get("address")}

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32601, "message": f"Method not found: {req.method}"}
                }

            print(f"[PID:{os.getpid()}] Request {req.method} completed successfully", file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": result
            }

        except httpx.TimeoutException:
            print(f"[PID:{os.getpid()}] Request {req.method} timed out", file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32000, "message": "Backend request timed out"}
            }
        except Exception as e:
            print(f"[PID:{os.getpid()}] Request {req.method} failed: {str(e)}", file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32000, "message": str(e)}
            }

    return app