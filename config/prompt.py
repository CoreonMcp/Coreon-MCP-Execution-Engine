from typing import Dict

def generate_llm_system_prompt(tool_registry: Dict) -> str:
    lines = [
        "You are an intelligent MCP agent. Users will provide natural language inputs.",
        "Your job is to convert the user's intent into a structured sequence of ToolCalls.",
        "",
        "Each ToolCall should contain:",
        "- tool: the tool name (e.g., \"nft\")",
        "- function: the function name (e.g., \"get_balance\")",
        "- params: a dictionary of parameter key-value pairs",
        "",
        "💡 Important Notes:",
        "- You must use **only the declared parameter names**. Do not invent or rename them.",
        "- Use `${stepX.field}` to reference the result of previous ToolCalls.",
        "- Always return a valid **JSON array** as your final output.",
        "",
        "=== Available Tools and Functions ==="
    ]

    for key, meta in tool_registry.items():
        tool, function = key.split(".", 1)
        param_names = meta.get("param_names", [])
        param_desc = meta.get("params", {})
        response_fields = meta.get("response_fields", {})  # 新增支持

        lines.append(f"- {tool}.{function}")
        if param_names:
            lines.append("  - params:")
            for param in param_names:
                desc = param_desc.get(param, {}).get("description", "")
                typ = param_desc.get(param, {}).get("type", "unknown")
                desc_part = f" ({typ})"
                if desc:
                    desc_part += f": {desc}"
                lines.append(f"    - {param}{desc_part}")
        if response_fields:
            lines.append("  - returns:")
            for field, meta_field in response_fields.items():
                typ = meta_field.get("type", "unknown")
                desc = meta_field.get("description", "")
                lines.append(f"    - {field} ({typ}): {desc}")
        if meta.get("usage_hint"):
            lines.append(f"  - usage: {meta['usage_hint']}")

    lines += [
        "- ToolCalls must be executed in sequence. The first call is step0, the second is step1, etc.",
        "- You may reference results from **previous** steps using `${stepX.field}`.",
        "- ❌ Do not reference the current or future steps (e.g., `${step1}` inside step1 is invalid)."
    ]

    return "\n".join(lines)