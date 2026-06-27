from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(__file__).parent

SANDBOX_TEMPLATE_NAME = "sandbox-agent"
SANDBOX_PACKAGES = ["PyPDF2"]

LLM_MODEL = "claude-opus-4-6"
MAX_TURNS = 30

SYSTEM_PROMPT = """\
You are an assistant operating a stateful Python REPL (a Jupyter kernel) inside an isolated sandbox.

You execute code by calling the `run_python` tool with a Python code block passed as a string.

Solve the user's task. The user may upload files or directories to /home/user/. Save any requested artifacts to /home/user/output/, which will be downloaded from the sandbox after completion.

A broad data-science stack is preinstalled (pandas, numpy, matplotlib, etc.). The sandbox does not have internet access, so you cannot install new packages. If you are unsure whether a package is available, just try importing it.
"""
