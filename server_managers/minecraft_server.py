import subprocess
import os
from typing import Optional
from .base_server import GameServer, logger

class MinecraftServer(GameServer):
    """Minecraft server implementation"""
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.executable_path = config.get('executable_path')
        self.memory = config.get('memory', '2G')
        self.port = config.get('default_port', 25565)
        self.server_properties = config.get('server_properties', 'server.properties')
    
    def start(self) -> bool:
        """Start the Minecraft server"""
        if not self.executable_path or not os.path.exists(self.executable_path):
            logger.error(f"Minecraft server JAR not found: {self.executable_path}")
            return False
        
        try:
            # Parse memory setting (e.g., "2G" -> "-Xmx2G")
            memory_arg = f"-Xmx{self.memory}"
            
            # Minecraft server command
            cmd = [
                'java',
                memory_arg,
                '-jar',
                self.executable_path,
                'nogui'  # Run without GUI
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
            
            logger.info(f"Minecraft server started on port {self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting Minecraft server: {e}")
            return False