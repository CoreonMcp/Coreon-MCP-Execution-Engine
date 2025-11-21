#!/usr/bin/env python3
import json
import sys
import asyncio
import httpx
import os
from typing import Any, Dict, Optional, Union
from config.settings import settings
from tools.token.logic import get_native_balance, get_my_wallet_address
from tools.token.schema import GetWalletTokensParams

MCP_SERVER_URL = settings.PROXY_BASE_URL

class CoreonMCPServer:
    def __init__(self):
        self.initialized = False

    def log(self, message: str):

        print(f"[CoreonMCP] {message}", file=sys.stderr, flush=True)

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        icon_path = os.path.abspath("assets/icon.png")

        self.log("Initialize request received")
        self.initialized = True

        return {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "coreon-mcp-server",
                "version": "1.0.0",
                "icon": f"file://{icon_path}"
            }
        }

    async def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tools": [
                {
                    "name": "get_balance",
                    "description": "Get wallet balance",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "wallet": {
                                "type": "string",
                                "description": "Wallet address"
                            }
                        },
                        "required": ["wallet"]
                    }
                },
                {
                    "name": "get_wallet_address",
                    "description": "Get wallet address",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }

    async def handle_prompts_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.log("Prompts list request received")
        return {
            "prompts": []
        }

    async def handle_resources_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.log("Resources list request received")
        return {
            "resources": []
        }

    async def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        self.log(f"Tool call: {tool_name} with args: {arguments}")

        try:
            if tool_name == "get_balance":
                wallet = arguments.get("wallet") or params.get("wallet")
                if not wallet:
                    raise ValueError("Missing wallet parameter1111")

                params = GetWalletTokensParams(address=wallet)
                data = await get_native_balance(params)
                balance = data.get("data", {}).get("balance")

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Balance: {balance}"
                        }
                    ]
                }

            elif tool_name == "get_wallet_address":
                address = await get_my_wallet_address()
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Wallet address: {address}"
                        }
                    ]
                }

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

        except httpx.HTTPError as e:
            self.log(f"HTTP error: {e}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Backend service error: {str(e)}"
                    }
                ],
                "isError": True
            }
        except Exception as e:
            self.log(f"Tool execution error: {e}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }
                ],
                "isError": True
            }

    def create_response(self, request_id: Optional[Union[str, int]], result: Any = None, error: Any = None) -> Dict[
        str, Any]:
        response = {
            "jsonrpc": "2.0",
            "id": request_id if request_id is not None else 1
        }

        if error is not None:
            response["error"] = error
        else:
            response["result"] = result

        return response

    async def handle_notification(self, method: str, params: Dict[str, Any]):
        self.log(f"Received notification: {method}")
        if method == "notifications/initialized":
            self.log("Client initialization complete")

    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if request_id is None:
            await self.handle_notification(method, params)
            return None

        self.log(f"Received method: {method} (id: {request_id})")

        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_tools_list(params)
            elif method == "prompts/list":
                result = await self.handle_prompts_list(params)
            elif method == "resources/list":
                result = await self.handle_resources_list(params)
            elif method == "tools/call":
                result = await self.handle_tools_call(params)
            else:
                error = {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
                return self.create_response(request_id, error=error)

            return self.create_response(request_id, result=result)

        except Exception as e:
            self.log(f"Error handling {method}: {e}")
            error = {
                "code": -32000,
                "message": str(e)
            }
            return self.create_response(request_id, error=error)

    async def run(self):
        self.log("Coreon MCP Server starting...")

        try:
            while True:
                try:
                    line = await asyncio.get_event_loop().run_in_executor(
                        None, sys.stdin.readline
                    )

                    if not line:
                        self.log("EOF received, shutting down")
                        break

                    line = line.strip()
                    if not line:
                        continue

                    self.log(f"Received: {line}")

                    try:
                        request = json.loads(line)
                        response = await self.handle_request(request)

                        if response is not None:
                            response_json = json.dumps(response)
                            self.log(f"Sending: {response_json}")
                            print(response_json, flush=True)

                    except json.JSONDecodeError as e:
                        self.log(f"JSON decode error: {e}")
                        error_response = self.create_response(
                            None,
                            error={"code": -32700, "message": "Parse error"}
                        )
                        print(json.dumps(error_response), flush=True)

                except Exception as e:
                    self.log(f"Read error: {e}")
                    break

        except Exception as e:
            self.log(f"Server error: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")

        self.log("Server shutting down")


async def main():
    server = CoreonMCPServer()
    await server.run()
