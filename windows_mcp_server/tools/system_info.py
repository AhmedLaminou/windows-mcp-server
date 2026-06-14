import platform
import datetime
import psutil
from windows_mcp_server.registry import windows_mcp_tool

@windows_mcp_tool()
def get_system_info() -> str:
    """Retrieve fundamental Windows system information (OS version, PC name, Uptime)."""
    uname = platform.uname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    return (f"OS: {uname.system} {uname.release} (Version: {uname.version})\n"
            f"PC Name: {uname.node}\nArchitecture: {uname.machine}\n"
            f"Processor: {uname.processor}\nBoot Time: {boot_time}\nUptime: {uptime}")

@windows_mcp_tool()
def get_hardware_info() -> str:
    """Retrieve deep hardware specifications including CPU, RAM limits, and disk geometries."""
    mem = psutil.virtual_memory()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    
    res = [
        f"CPU Cores: {cpu_cores} (Logical: {cpu_threads})",
        f"CPU Freq: {cpu_freq.current:.2f}MHz (Max: {cpu_freq.max:.2f}MHz)" if cpu_freq else "CPU Freq: Unknown",
        f"Memory Total: {mem.total / (1024**3):.2f} GB",
        f"Memory Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)"
    ]
    
    res.append("\nDisks:")
    for part in psutil.disk_partitions(all=False):
        if 'cdrom' in part.opts or part.fstype == '': continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            res.append(f"  {part.device} [{part.fstype}] {usage.used/(1024**3):.1f}GB / {usage.total/(1024**3):.1f}GB ({usage.percent}%)")
        except PermissionError: pass
        
    return "\n".join(res)
