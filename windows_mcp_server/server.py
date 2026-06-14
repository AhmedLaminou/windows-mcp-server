from mcp.server.fastmcp import FastMCP
from windows_mcp_server.registry import register_all_tools

# Create a FastMCP server without unsupported arguments like 'description'
mcp = FastMCP("Windows Task Manager")

# Register all tools from the registry
register_all_tools(mcp)

def main():
    """Entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
