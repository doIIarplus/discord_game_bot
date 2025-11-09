import subprocess
import os
from typing import Optional
from .base_server import GameServer, logger

class FactorioServer(GameServer):
    """Factorio server implementation"""
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.executable_path = config.get('executable_path')
        self.port = config.get('default_port', 34197)
        self.server_settings = config.get('server_settings', 'server-settings.json')
        self.game_port = config.get('game_port', 34197)
        
    def start(self) -> bool:
        """Start the Factorio server"""
        if not self.executable_path or not os.path.exists(self.executable_path):
            logger.error(f"Factorio server executable not found: {self.executable_path}")
            return False
        
        try:
            # Factorio server command arguments
            cmd = [
                self.executable_path,
                '--start-server',
                '--port', str(self.game_port),
                '--server-settings', self.server_settings
            ]
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.executable_path) if os.path.dirname(self.executable_path) else '.'
            )
            
            # Start monitoring after a brief delay to ensure process is running
            if self.process.pid:
                import time
                time.sleep(1)  # Wait a bit for the process to fully start
                self.start_monitoring()
            
            logger.info(f"Factorio server started on port {self.game_port}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting Factorio server: {e}")
            return False