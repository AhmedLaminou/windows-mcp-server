registered_tools = []

def windows_mcp_tool():
    """
    Decorator to register a function as a Windows MCP tool.
    """
    def decorator(func):
        registered_tools.append(func)
        return func
    return decorator

def register_all_tools(mcp):
    """
    Imports all tool modules and registers them with the FastMCP instance.
    """
    import windows_mcp_server.tools.execute_powershell
    import windows_mcp_server.tools.manage_registry
    import windows_mcp_server.tools.manage_network
    import windows_mcp_server.tools.task_manager
    import windows_mcp_server.tools.software_audit
    import windows_mcp_server.tools.storage_analysis
    import windows_mcp_server.tools.system_info
    import windows_mcp_server.tools.process_management
    import windows_mcp_server.tools.optimization
    import windows_mcp_server.tools.services
    import windows_mcp_server.tools.hardware_drivers
    import windows_mcp_server.tools.media_management
    import windows_mcp_server.tools.advanced_process
    import windows_mcp_server.tools.window_management
    import windows_mcp_server.tools.startup_tasks
    import windows_mcp_server.tools.event_diagnostics
    import windows_mcp_server.tools.network_diagnostics
    import windows_mcp_server.tools.security_updates
    import windows_mcp_server.tools.power_hardware
    import windows_mcp_server.tools.safe_file_operations
    import windows_mcp_server.tools.developer_environment
    import windows_mcp_server.tools.shell_helpers
    import windows_mcp_server.tools.disk_health
    import windows_mcp_server.tools.driver_maintenance
    import windows_mcp_server.tools.software_maintenance
    import windows_mcp_server.tools.peripherals
    import windows_mcp_server.tools.virtualization
    import windows_mcp_server.tools.restore_update_controls

    for func in registered_tools:
        mcp.tool()(func)
