import datetime
import os
import subprocess
from typing import Optional

import psutil

from windows_mcp_server.registry import windows_mcp_tool


def _format_time(timestamp: float) -> str:
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def _signature_status(exe_path: Optional[str]) -> str:
    if not exe_path or not os.path.exists(exe_path):
        return "Unknown"

    escaped_path = exe_path.replace("'", "''")
    ps_cmd = (
        "Get-AuthenticodeSignature -LiteralPath "
        f"'{escaped_path}' | "
        "Select-Object Status,SignerCertificate | ConvertTo-Json -Depth 3"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return "Unknown"
        return result.stdout.strip()
    except Exception:
        return "Unknown"


@windows_mcp_tool()
def get_process_details(pid: int) -> str:
    """
    Return detailed process metadata for a PID, including command line, parent,
    executable path, resource usage, open files, network connections, and signature status.
    """
    try:
        proc = psutil.Process(pid)
        with proc.oneshot():
            parent = proc.parent()
            memory = proc.memory_info()
            cpu_times = proc.cpu_times()
            exe_path = proc.exe() if proc.exe else ""
            lines = [
                f"Name: {proc.name()}",
                f"PID: {proc.pid}",
                f"Status: {proc.status()}",
                f"User: {proc.username()}",
                f"Created: {_format_time(proc.create_time())}",
                f"Parent: {parent.name()} (PID: {parent.pid})" if parent else "Parent: None",
                f"Executable: {exe_path}",
                f"Command Line: {' '.join(proc.cmdline())}",
                f"Working Directory: {proc.cwd()}",
                f"Threads: {proc.num_threads()}",
                f"Handles: {proc.num_handles() if hasattr(proc, 'num_handles') else 'Unknown'}",
                f"CPU Time: user={cpu_times.user:.2f}s system={cpu_times.system:.2f}s",
                f"Memory RSS: {memory.rss / (1024 ** 2):.2f} MB",
                f"Memory VMS: {memory.vms / (1024 ** 2):.2f} MB",
                f"Signature: {_signature_status(exe_path)}",
            ]

            try:
                open_files = proc.open_files()
                lines.append("\nOpen Files:")
                lines.extend(f"  {file.path}" for file in open_files[:20])
                if len(open_files) > 20:
                    lines.append(f"  ... and {len(open_files) - 20} more")
            except Exception as exc:
                lines.append(f"\nOpen Files: unavailable ({exc})")

            try:
                connections = proc.net_connections(kind="inet")
                lines.append("\nNetwork Connections:")
                for conn in connections[:20]:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
                    lines.append(f"  {laddr} -> {raddr} [{conn.status}]")
                if len(connections) > 20:
                    lines.append(f"  ... and {len(connections) - 20} more")
            except Exception as exc:
                lines.append(f"\nNetwork Connections: unavailable ({exc})")

            return "\n".join(lines)
    except psutil.NoSuchProcess:
        return f"Error: No process found with PID {pid}."
    except psutil.AccessDenied:
        return f"Error: Access denied reading process PID {pid}."
    except Exception as exc:
        return f"Error getting process details: {exc}"


@windows_mcp_tool()
def get_process_tree(pid: int = 0) -> str:
    """
    Show parent-child process relationships.
    Args:
        pid: Root PID to inspect. Use 0 to show top-level process trees.
    """
    try:
        processes = {proc.pid: proc for proc in psutil.process_iter(["pid", "name", "ppid"])}
        children: dict[int, list[psutil.Process]] = {}
        for proc in processes.values():
            try:
                children.setdefault(proc.ppid(), []).append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        roots = [processes[pid]] if pid else [
            proc for proc in processes.values() if proc.ppid() not in processes
        ]

        lines: list[str] = []

        def walk(proc: psutil.Process, depth: int) -> None:
            try:
                indent = "  " * depth
                lines.append(f"{indent}- {proc.name()} (PID: {proc.pid})")
                for child in sorted(children.get(proc.pid, []), key=lambda item: item.name().lower()):
                    walk(child, depth + 1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return

        for root in sorted(roots, key=lambda item: item.name().lower()):
            walk(root, 0)

        return "\n".join(lines[:500]) if lines else "No process tree data found."
    except KeyError:
        return f"Error: No process found with PID {pid}."
    except Exception as exc:
        return f"Error building process tree: {exc}"


@windows_mcp_tool()
def find_process_locking_file(file_path: str) -> str:
    """
    Identify processes that appear to have a file open.
    Note: Windows may hide some handles without Administrator privileges.
    """
    target = os.path.abspath(file_path).lower()
    matches: list[str] = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            for open_file in proc.open_files():
                if os.path.abspath(open_file.path).lower() == target:
                    matches.append(f"PID: {proc.pid} | Name: {proc.name()} | Path: {open_file.path}")
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception:
            continue

    if matches:
        return "\n".join(matches)
    return f"No visible process handles found for '{file_path}'. Try running as Administrator for deeper handle visibility."
