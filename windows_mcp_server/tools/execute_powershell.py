import subprocess
from windows_mcp_server.registry import windows_mcp_tool

@windows_mcp_tool()
def execute_powershell(script: str, require_admin: bool = False) -> str:
    """
    Execute a PowerShell script or command.
    Use this for advanced system management tasks not covered by other tools.
    
    Args:
        script: The PowerShell script to execute.
        require_admin: If true, attempts to run with elevated privileges (requires UAC prompt if not already elevated).
    """
    try:
        if require_admin:
            command = f"Start-Process powershell -ArgumentList '-NoProfile -NonInteractive -Command \"{script}\"' -Verb RunAs -Wait"
            result = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True)
            return "Command executed with elevated privileges. Check system state for results."
        else:
            result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip() if result.stdout else "Command completed successfully with no output."
            else:
                return f"Error executing PowerShell (Exit {result.returncode}):\n{result.stderr.strip()}"
    except Exception as e:
        return f"Exception executing PowerShell: {str(e)}"
