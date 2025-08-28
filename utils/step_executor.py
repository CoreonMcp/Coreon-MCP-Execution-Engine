from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from utils.logging_utils import log_trace
import importlib
import json

console = Console()

def _fmt_source(src):
    if not src:
        return None
    if isinstance(src, (list, tuple, set)):
        return ", ".join(map(str, src))
    return str(src)

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
            title="[green]Executing ToolCall",
            subtitle=f"[dim]{call.get('tool')}",
            box=box.ROUNDED,
        ))

        try:
            result = await execute_toolcall(call, registry, context)
            log_trace(f"EXECUTOR STEP {i} RESULT:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        except Exception as e:
            console.print(f"[bold red]❌ Error:[/bold red] {str(e)}\n")
            results.append({"step": step_key, "call": call})
            continue

        call_result = result.get("result", {})
        # 预览行
        preview = str(call_result)
        preview = (preview[:50] + ".........") if len(preview) > 50 else preview
        status_icon = "✅" if result.get("ok", True) else "❌"

        console.print(f"{status_icon} [bold]Result:[/bold] {preview}")

        src = _fmt_source(meta.get("source"))
        if src:
            console.print(f"[bold]📡 Source: {src}[bold]")

        console.print()

        if isinstance(call_result, dict):
            context[step_key] = call_result.get("data", call_result)

        results.append({
            "step": step_key,
            "call": call,
            "result": call_result,
        })

    return results