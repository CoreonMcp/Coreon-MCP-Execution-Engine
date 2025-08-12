from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from utils.logging_utils import log_trace
import importlib
import json

console = Console()

async def execute_step_chain(calls, registry, context, execute_toolcall):
    results = []

    for i, call in enumerate(calls):
        meta = registry[call["tool"]]

        module = importlib.import_module(meta["module"])
        func = getattr(module, meta["function"])

        step_key = f"step{i}"
        step_title = f"Step {i+1}: {func.__name__}"

        console.print(Panel.fit(
            Text(f"🧩 {step_title}", style="bold cyan"),
            title=f"[green]Executing ToolCall",
            subtitle=f"[dim]{call.get('tool')}",
            box=box.ROUNDED,
        ))

        try:
            result = await execute_toolcall(call, registry, context)
            log_trace(f"EXECUTOR STEP {i} RESULT:\n{json.dumps(result, indent=2)}")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/bold red] {str(e)}\n")
            results.append({
                "step": step_key,
                "call": call,
            })
            continue

        call_result = result.get("result", {})
        strs = str(call_result)[:50]
        result_preview = f"{strs}........."
        status_icon = "✅" if result.get("ok", True) else "❌"

        console.print(f"{status_icon} [bold]Result:[/bold] {result_preview}\n")

        if isinstance(call_result, dict):
            context[step_key] = call_result.get("data", call_result)

        results.append({
            "step": step_key,
            "call": call,
            "result": call_result,
        })

    return results
