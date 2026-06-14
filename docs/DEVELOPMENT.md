# Development Guide

## Local Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
```

## Run the Server

```powershell
windows-mcp-server
```

or:

```powershell
python -m windows_mcp_server.server
```

## Verify Python

```powershell
.\venv\Scripts\python.exe -m compileall windows_mcp_server
```

## Verify Registered Tools

```powershell
.\venv\Scripts\python.exe -c "from windows_mcp_server.registry import register_all_tools, registered_tools; Dummy=type('Dummy',(),{'tool':lambda self: (lambda f:f)}); register_all_tools(Dummy()); print(len(registered_tools))"
```

Expected count: `96`.

## Verify VS Code Extension

```powershell
cd vscode-extension
npm install
npm run compile
```

## Adding a Tool

1. Create or update a module under `windows_mcp_server/tools/`.
2. Decorate the function with `@windows_mcp_tool()`.
3. Import the module in `windows_mcp_server/registry.py`.
4. Run the compile and tool-count checks.
5. Update `docs/TOOLS.md` and the README capability summary.

Prefer read-only tools or dry-run defaults for system-changing workflows.
