import subprocess
import psutil
import logging
import time
import threading
import asyncio
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger('GameServerBot')

class GameServer:
    """Base class for managing game servers"""
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.pid: Optional[int] = None
        self.logs: List[str] = []
        self.log_thread: Optional[threading.Thread] = None
        self.monitoring = False
        self.cpu_percent = 0
        self.memory_percent = 0
        self.memory_info = None
        
    def start(self) -> bool:
        """Start the game server"""
        raise NotImplementedError("Subclasses must implement start method")
    
    def stop(self) -> bool:
        """Stop the game server"""
        if self.process and self.process.poll() is None:
            try:
                # Stop monitoring before stopping the process
                self.stop_monitoring()
                
                # Try graceful shutdown first
                self.process.terminate()
                # Wait a bit for graceful shutdown
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't shut down gracefully
                    self.process.kill()
                    self.process.wait()
                
                self.is_running = False
                self.pid = None
                logger.info(f"{self.name} server stopped")
                return True
            except Exception as e:
                logger.error(f"Error stopping {self.name} server: {e}")
                return False
        else:
            # Even if process is not running, stop monitoring
            self.stop_monitoring()
        return True  # Already stopped
    
    def restart(self) -> bool:
        """Restart the game server"""
        self.stop()
        time.sleep(2)  # Give some time before restarting
        return self.start()
    
    def get_status(self) -> dict:
        """Get server status"""
        status = {
            'name': self.name,
            'running': self.is_running,
            'pid': self.pid,
            'port': self.config.get('default_port', 'N/A')
        }
        
        # Add monitoring data if available
        if self.monitoring:
            status['monitoring_data'] = self.get_monitoring_data()
        else:
            status['monitoring_data'] = None
            
        return status
    
    def is_process_running(self) -> bool:
        """Check if the server process is actually running"""
        if self.pid is None:
            return False
        
        try:
            process = psutil.Process(self.pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def start_monitoring(self):
        """Start monitoring the server process"""
        if not self.pid:
            return False
        
        try:
            self.system_process = psutil.Process(self.pid)
            self.monitoring = True
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def stop_monitoring(self):
        """Stop monitoring the server process"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Internal monitoring loop"""
        while self.monitoring:
            try:
                if self.system_process and self.system_process.is_running():
                    # Get CPU and memory usage
                    self.cpu_percent = self.system_process.cpu_percent()
                    self.memory_info = self.system_process.memory_info()
                    self.memory_percent = self.system_process.memory_percent()
                else:
                    self.cpu_percent = 0
                    self.memory_percent = 0
                    self.memory_info = None
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process may have died, reset metrics
                self.cpu_percent = 0
                self.memory_percent = 0
                self.memory_info = None
            
            # Sleep for a bit before next check (monitoring interval)
            time.sleep(5)
    
    def get_monitoring_data(self) -> dict:
        """Get current monitoring data"""
        return {
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_rss': self.memory_info.rss if self.memory_info else 0,
            'memory_vms': self.memory_info.vms if self.memory_info else 0,
            'monitoring': self.monitoring
        }

class ServerManager:
    """Manages all game servers"""
    def __init__(self, config: dict):
        self.config = config
        self.servers: Dict[str, GameServer] = {}
        self.server_classes = {}
        
        # Register available server types
        from .terraria_server import TerrariaServer
        from .minecraft_server import MinecraftServer
        from .factorio_server import FactorioServer
        from .necesse_server import NecesseServer
        
        self.server_classes['terraria'] = TerrariaServer
        self.server_classes['minecraft'] = MinecraftServer
        self.server_classes['factorio'] = FactorioServer
        self.server_classes['necesse'] = NecesseServer
    
    def create_server(self, game_type: str, name: str = None) -> Optional[GameServer]:
        """Create a server instance"""
        if game_type not in self.server_classes:
            logger.error(f"Unsupported game type: {game_type}")
            return None
        
        if name is None:
            name = game_type
            
        config = self.config.get('games', {}).get(game_type, {})
        if not config:
            logger.error(f"No configuration found for game type: {game_type}")
            return None
        
        server = self.server_classes[game_type](name, config)
        self.servers[name] = server
        return server
    
    def get_server(self, name: str) -> Optional[GameServer]:
        """Get a server by name"""
        return self.servers.get(name)
    
    def start_server(self, name: str) -> bool:
        """Start a server by name"""
        server = self.get_server(name)
        if server:
            # Check if already running
            if server.is_running and server.is_process_running():
                logger.info(f"{name} server is already running")
                return False
            
            success = server.start()
            if success:
                server.is_running = True
                if server.process:
                    server.pid = server.process.pid
            return success
        else:
            logger.error(f"Server {name} not found")
            return False
    
    def stop_server(self, name: str) -> bool:
        """Stop a server by name"""
        server = self.get_server(name)
        if server:
            success = server.stop()
            server.is_running = False
            return success
        else:
            logger.error(f"Server {name} not found")
            return False
    
    def restart_server(self, name: str) -> bool:
        """Restart a server by name"""
        server = self.get_server(name)
        if server:
            success = server.restart()
            server.is_running = success
            if success and server.process:
                server.pid = server.process.pid
            return success
        else:
            logger.error(f"Server {name} not found")
            return False
    
    def get_status(self, name: str = None) -> Dict:
        """Get status of all servers or specific server"""
        if name:
            server = self.get_server(name)
            if server:
                return server.get_status()
            else:
                return {'error': f'Server {name} not found'}
        else:
            statuses = {}
            for name, server in self.servers.items():
                statuses[name] = server.get_status()
            return statuses
    
    def list_servers(self) -> List[str]:
        """Get list of all managed servers"""
        return list(self.servers.keys())
    
    def get_available_games(self) -> List[str]:
        """Get list of available game types"""
        return list(self.server_classes.keys())