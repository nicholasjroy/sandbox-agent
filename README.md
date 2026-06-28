# sandbox-agent

Lightweight `ClaudeSDKClient` agent that executes code in an isolated E2B sandbox to solve a user-defined task.

Since the agent loop runs locally and a single `run_python` tool forwards the agent's code to the sandbox, no secrets (like `ANTHROPIC_API_KEY`) are exposed to it. The user can optionally upload local directories to `/home/user/` in the sandbox, and any files the agent writes to `/home/user/output/` (e.g., final answer markdowns, CSVs) are automatically downloaded.

## Setup

Requires Python 3.12+.

​```bash
uv sync
​```

Create a `.env` file with your API keys:

​```
ANTHROPIC_API_KEY=...
E2B_API_KEY=...
​```

## Usage

Run the agent in the CLI, optionally uploading a directory into the sandbox:

​```bash
uv run python -m sandbox_agent.cli --task "<task>" --directory <path>
​```

The agent's transcript and any downloaded artifacts are written to `runs/<timestamp>/` in the project root. The first time this is called, E2B will build the template (which gets reused by subsequent sessions).

Settings such as the Anthropic model, system prompt, and sandbox packages can be adjusted in `sandbox_agent/config.py`. When changing the sandbox packages, the template needs to be rebuilt:

```bash
uv run python -c "from sandbox_agent.template import build_template; build_template()"
```
