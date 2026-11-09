# Changelog

## Unreleased

### Fixed

- **Compatibility with `mcp` 2.x.** The MCP Python SDK v2 (released 2026-07-28)
  renamed `FastMCP` to `MCPServer` and removed the `mcp.server.fastmcp` module
  with no deprecation shim, so a fresh `pip install` crashed on start-up with
  `ModuleNotFoundError`. `server.py` now imports `MCPServer` from
  `mcp.server.mcpserver` and falls back to `FastMCP` on `mcp` 1.x.
- Removed the unused `fastmcp` dependency (the standalone package was never
  imported; the server always used the SDK's built-in class).

### Changed

- Dependency range is now `mcp>=1.12,<3` so the next major release cannot break
  installs silently again.
- Server name shown to clients is now `Windows Management` and the package
  version is reported in the MCP `serverInfo`.
- CI runs on Python 3.10 and 3.13 against both `mcp` 1.x and `mcp` 2.x.

### Added

- `tests/` with import, tool-count and `list_tools()` checks (they can also be
  run on Linux/macOS thanks to a `conftest.py` that stubs `winreg`/`windll`).

## 0.3.0

- Expanded the server to 96 Windows management tools.
- Added storage cleanup reports and safer Recycle Bin deletion workflows.
- Added GPU, driver, disk health, Windows Update, restore point, WSL, Hyper-V, printer, audio, Bluetooth, firewall, and uninstall maintenance tools.
- Added VS Code extension wrapper.
- Added MCP Registry metadata and publishing documentation.
