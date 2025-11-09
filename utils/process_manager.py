import psutil
import subprocess
from typing import Optional, List

class ProcessManager:
    """Utility class for managing processes"""
    
    @staticmethod
    def is_port_in_use(port: int) -> bool:
        """Check if a port is currently in use"""
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.status in ['LISTEN', 'ESTABLISHED']:
                    return True
            return False
        except Exception:
            # Fallback - if we can't check, assume it's not in use
            return False
    
    @staticmethod
    def kill_process_by_port(port: int) -> bool:
        """Kill any process using a specific port"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                connections = proc.info.get('connections', [])
                for conn in connections:
                    if conn.laddr.port == port:
                        proc.kill()
                        return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_process_by_pid(pid: int) -> Optional[psutil.Process]:
        """Get process by PID"""
        try:
            return psutil.Process(pid)
        except psutil.NoSuchProcess:
            return None
    
    @staticmethod
    def is_process_running(pid: int) -> bool:
        """Check if a process with given PID is running"""
        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False