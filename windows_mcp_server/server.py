"""Entry point for the Windows Management MCP server.

This module works with both generations of the official MCP Python SDK:

* ``mcp >= 2.0``  -> ``MCPServer`` (``mcp.server.mcpserver``).
  In v2 the old ``FastMCP`` class was renamed to ``MCPServer`` and the
  ``mcp.server.fastmcp`` module was removed without a deprecation shim.
* ``mcp 1.x``     -> ``FastMCP`` (``mcp.server.fastmcp``).

Migration guide:
https://py.sdk.modelcontextprotocol.io/v2/migration/#fastmcp-renamed-to-mcpserver
"""

from importlib.metadata import PackageNotFoundError, version as _dist_version

from windows_mcp_server.registry import register_all_tools

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server

    _SDK_GENERATION = 2
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server

    _SDK_GENERATION = 1

SERVER_NAME = "Windows Management"


def _package_version() -> str:
    try:
        return _dist_version("windows-management-mcp-server")
    except PackageNotFoundError:  # running from a source checkout
        return "0.0.0+local"


def create_server():
    """Build the MCP server and register every Windows tool on it."""
    if _SDK_GENERATION == 2:
        # In v2 only `name` is positional-safe: pass everything else by keyword.
        server = _Server(SERVER_NAME, version=_package_version())
    else:
        server = _Server(SERVER_NAME)
    register_all_tools(server)
    return server


mcp = create_server()


def main():
    """Run the server over stdio (the default transport)."""
    mcp.run()


if __name__ == "__main__":
    main()
