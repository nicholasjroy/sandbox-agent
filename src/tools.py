from claude_agent_sdk import create_sdk_mcp_server, tool

MAX_CHARS = 8_000


def _trim(text: str) -> str:
    if len(text) <= MAX_CHARS:
        return text
    head = MAX_CHARS // 2
    tail = MAX_CHARS - head
    omitted = len(text) - MAX_CHARS
    return f"{text[:head]}\n\n... [truncated {omitted} chars] ...\n\n{text[-tail:]}"


def build_mcp(sandbox):
    @tool(
        "run_python",
        "Execute Python in a stateful Jupyter kernel. "
        "Returns stdout, stderr, the final line's value, and any error.",
        {"code": str},
    )
    async def run_python(args):
        ex = await sandbox.run_code(args["code"])
        has_error = ex.error is not None

        parts = []
        if ex.logs.stdout:
            parts.append(f"STDOUT:\n{_trim(''.join(ex.logs.stdout))}")
        if ex.logs.stderr:
            parts.append(f"STDERR:\n{_trim(''.join(ex.logs.stderr))}")
        if ex.text:
            parts.append(f"RESULT:\n{_trim(ex.text)}")
        if has_error:
            parts.append(f"ERROR: {ex.error.name}: {ex.error.value}\n{_trim(ex.error.traceback)}")

        text = "\n\n".join(parts) or "(no output)"
        return {"content": [{"type": "text", "text": text}], "is_error": has_error}

    return create_sdk_mcp_server(name="e2b", version="1.0.0", tools=[run_python])