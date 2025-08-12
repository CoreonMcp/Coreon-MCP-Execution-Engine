import importlib
import re
import inspect
from typing import Dict, Any
from utils.step_executor import execute_step_chain

async def execute_toolcall(call: Dict[str, Any], registry: Dict[str, Dict], context: Dict[str, Any] = {}) -> Dict:
    try:
        meta = registry[call["tool"]]

        module = importlib.import_module(meta["module"])
        func = getattr(module, meta["function"])

        raw_params = call.get("params", {})
        resolved_params = resolve_params_with_conte(raw_params, context)

        source = context.get("source", "unknown")
        resolved_params["source"] = source

        if "schema" in meta and meta["schema"]:
            schema_class = meta["schema"]
            validated_params = schema_class(**resolved_params)
        else:
            validated_params = resolved_params

        if callable(func):
            sig = inspect.signature(func)
            if len(sig.parameters) == 0:
                result = await func()
            elif isinstance(validated_params, dict):
                result = await func(**validated_params)
            else:
                result = await func(validated_params)
            return {"call": call, "result": result}
        else:
            return {"call": call, "result": {"error": "Function is not callable"}}

    except Exception as e:
        return {"call": call, "result": {"error": str(e)}}

async def execute_toolcall_chain(calls: list, registry: Dict[str, Dict], context: Dict[str, Any] = {}) -> list:
    context = {}

    return await execute_step_chain(calls, registry, context, execute_toolcall)

def resolve_params_with_conte(params: Dict[str, Any], context: dict) -> dict:
    pattern = re.compile(r"\$\{(step\d+)\.([a-zA-Z0-9_]+)\}")
    resolved = {}

    for k, v in params.items():
        if isinstance(v, str):
            match = pattern.fullmatch(v)
            if match:
                step_key, field = match.groups()
                v = context.get(step_key, {}).get(field)
        resolved[k] = v

    return resolved