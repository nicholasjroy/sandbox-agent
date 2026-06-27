from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)
from e2b_code_interpreter import AsyncSandbox
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax

from config import LLM_MODEL, MAX_TURNS, SYSTEM_PROMPT
from src.tools import build_mcp


def _flatten_text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") for part in content or [])


async def run_agent(task: str, sandbox: AsyncSandbox) -> str:
    options = ClaudeAgentOptions(
        model=LLM_MODEL,
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"e2b": build_mcp(sandbox)},
        allowed_tools=["mcp__e2b__*"],
        tools=[],
        max_turns=MAX_TURNS,
    )

    console = Console(record=True)
    turn = 0
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Task: " +task)
        console.print(Rule("Start", style="dark_orange"))
        async for msg in client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        console.print(Panel(block.text, title="assistant", border_style="cyan"))
                    elif isinstance(block, ToolUseBlock) and block.name.endswith("run_python"):
                        turn += 1
                        console.print(Rule(f"Turn {turn}", style="yellow"))
                        code = Syntax(block.input["code"], "python", word_wrap=True)
                        console.print(Panel(code, title="run_python", border_style="blue"))
            elif isinstance(msg, UserMessage):
                for block in msg.content:
                    if isinstance(block, ToolResultBlock):
                        text = _flatten_text(block.content)
                        style = "red" if block.is_error else "green"
                        console.print(Panel(text, title="output", border_style=style))

    return console.export_text()
