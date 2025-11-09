import subprocess
import os
from typing import Optional
from .base_server import GameServer, logger

class TerrariaServer(GameServer):
    """Terraria server implementation"""
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.executable_path = config.get('executable_path')
        self.port = config.get('default_port', 7777)
        self.world = config.get('default_world', 'world.wld')
    
    def start(self) -> bool:
        """Start the Terraria server"""
        if not self.executable_path or not os.path.exists(self.executable_path):
            logger.error(f"Terraria server executable not found: {self.executable_path}")
            return False
        
        try:
            # Terraria server command arguments
            cmd = [
                self.executable_path,
                '-port', str(self.port),
                '-world', self.world,
                '-autocreate', '3',  # Create world if doesn't exist (0=small, 1=medium, 2=large, 3=experimental)
                '-maxplayers', '8',  # Default max players
                '-difficulty', '0',  # 0=classic, 1=expert, 2=master, 3=journey
                '-worldname', 'TerrariaWorld'
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
                time.sleep(1)  # Wait a bit for the process to fully start
                self.start_monitoring()
            
            logger.info(f"Terraria server started on port {self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting Terraria server: {e}")
            return False