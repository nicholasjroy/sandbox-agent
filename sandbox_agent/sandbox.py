from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path, PurePosixPath

from e2b import FileType
from e2b_code_interpreter import AsyncSandbox

from sandbox_agent.config import SANDBOX_TEMPLATE_NAME

SANDBOX_TIMEOUT = 3_600  # 1hr

IGNORE = {
    ".git",
    ".env",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".DS_Store",
    "Thumbs.db",
}


async def create_sandbox() -> AsyncSandbox:
    return await AsyncSandbox.create(
        template=SANDBOX_TEMPLATE_NAME,
        timeout=SANDBOX_TIMEOUT,
        allow_internet_access=False,
    )


@asynccontextmanager
async def sandbox_session() -> AsyncIterator[AsyncSandbox]:
    sandbox = await create_sandbox()
    try:
        yield sandbox
    finally:
        await sandbox.kill()


async def upload_dir(sandbox: AsyncSandbox, dir: Path) -> None:
    """Upload every file under `dir` into `/home/user`."""
    files = []
    for path in dir.rglob("*"):
        relative = path.relative_to(dir)
        if not path.is_file() or any(part in IGNORE for part in relative.parts):
            continue
        files.append({"path": f"/home/user/{relative.as_posix()}", "data": path.read_bytes()})

    if files:
        await sandbox.files.write_files(files)


async def download_outputs(sandbox: AsyncSandbox, dir: Path) -> None:
    """Save every file under `/home/user/output` into `dir`."""
    output_dir = "/home/user/output"
    if not await sandbox.files.exists(output_dir):
        return

    for entry in await sandbox.files.list(output_dir, depth=None):
        if entry.type == FileType.DIR:
            continue
        relative = PurePosixPath(entry.path).relative_to(output_dir)
        local = dir.joinpath(*relative.parts)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(await sandbox.files.read(entry.path, format="bytes"))
