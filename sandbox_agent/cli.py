import asyncio
from datetime import datetime, timezone
from pathlib import Path

import typer

from sandbox_agent.config import PROJECT_DIR
from sandbox_agent.agent import run_agent
from sandbox_agent.sandbox import download_outputs, sandbox_session, upload_dir
from sandbox_agent.template import ensure_template

app = typer.Typer(add_completion=False)


async def main(task: str, directory: Path | None) -> None:
    ensure_template()
    async with sandbox_session() as sandbox:
        if directory is not None:
            await upload_dir(sandbox, directory)
        transcript = await run_agent(task, sandbox)

        run_dir = PROJECT_DIR / "runs" / datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "transcript.log").write_text(transcript, encoding="utf-8")
        await download_outputs(sandbox, run_dir)


@app.command()
def run(
    task: str = typer.Option(..., help="Task for the agent"),
    directory: Path | None = typer.Option(None, help="Directory uploaded into the sandbox."),
):
    asyncio.run(main(task, directory))


if __name__ == "__main__":
    app()
