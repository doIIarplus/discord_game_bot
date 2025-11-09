import subprocess
import os
from typing import Optional
from .base_server import GameServer, logger

class PalworldServer(GameServer):
    """Palworld server implementation"""
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.executable_path = config.get('executable_path')
        self.port = config.get('default_port', 8211)
        self.query_port = config.get('query_port', 27015)
        self.rcon_port = config.get('rcon_port', 25575)
        self.server_name = config.get('server_name', 'Palworld Server')
        self.max_players = config.get('max_players', 16)
        
    def start(self) -> bool:
        """Start the Palworld server"""
        if not self.executable_path or not os.path.exists(self.executable_path):
            logger.error(f"Palworld server executable not found: {self.executable_path}")
            return False
        
        try:
            # Palworld server command arguments
            cmd = [
                self.executable_path,
                f"ListenPort={self.port}",
                f"ServerName=\"{self.server_name}\"",
                f"MaxPlayersNum={self.max_players}",
                f"PublicPort={self.port}",
                f"RCONEnabled=True",
                f"RCONPort={self.rcon_port}",
                "bEnablePlayerToPlayerDamage=true",
                "bEnableFriendlyFire=true",
                "bEnableInvaderEnemy=true",
                "bActivePlusTime=false",
                "bEnableAimAssistPad=true",
                "bEnableAimAssistKeyboard=false",
                "bServerAuth=true",
                "bShowPlayerList=true",
                "RCONEnabled=True"
            ]
            
            # Add additional args from config if available
            additional_args = self.config.get('additional_args', [])
            if additional_args:
                cmd.extend(additional_args)
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.executable_path) if os.path.dirname(self.executable_path) else '.'
            )
            
            # Start monitoring after a brief delay to ensure process is running
            import time
            time.sleep(1)  # Wait a bit for the process to fully start
            self.start_monitoring()
            
            logger.info(f"Palworld server started on port {self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting Palworld server: {e}")
            return False