import subprocess
import os
from typing import Optional
from .base_server import GameServer, logger

class NecesseServer(GameServer):
    """Necesse server implementation for macOS/Linux"""
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.server_dir = config.get('server_dir')
        self.executable_path = config.get('executable_path')
        self.port = config.get('default_port', 14159)
        self.world_name = config.get('world_name', 'NecesseWorld')
        self.max_slots = config.get('max_slots', 8)
        self.server_password = config.get('server_password', '')
        self.owner_name = config.get('owner_name', '')
        self.use_local_dir = config.get('use_local_dir', True)

    def start(self) -> bool:
        """Start the Necesse server"""
        if not self.executable_path or not os.path.exists(self.executable_path):
            logger.error(f"Necesse server startup script not found: {self.executable_path}")
            logger.info(f"Please ensure the Necesse server is installed and the path is correct.")
            return False

        # Make sure the script is executable
        try:
            os.chmod(self.executable_path, 0o755)
        except Exception as e:
            logger.warning(f"Could not set execute permissions on {self.executable_path}: {e}")

        try:
            # Build the command with parameters
            # StartServer-nogui.sh already includes -nogui, so we just add our parameters
            cmd = [self.executable_path]

            # World name (required for non-interactive startup)
            cmd.extend(['-world', self.world_name])

            # Port configuration
            cmd.extend(['-port', str(self.port)])

            # Player slots
            cmd.extend(['-slots', str(self.max_slots)])

            # Server password (if set)
            if self.server_password:
                cmd.extend(['-password', self.server_password])

            # Owner name for auto-permissions (if set)
            if self.owner_name:
                cmd.extend(['-owner', self.owner_name])

            # Use local directory for configs/saves
            if self.use_local_dir:
                cmd.append('-localdir')

            # Pause when empty (helpful for resource management)
            cmd.extend(['-pausewhenempty', '1'])

            # Logging enabled
            cmd.extend(['-logging', '1'])

            logger.info(f"Starting Necesse server with command: {' '.join(cmd)}")

            # Determine working directory
            work_dir = self.server_dir if self.server_dir and os.path.exists(self.server_dir) else os.path.dirname(self.executable_path)

            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                cwd=work_dir,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )

            # Start monitoring after a brief delay to ensure process is running
            if self.process.pid:
                import time
                time.sleep(2)  # Wait for the process to fully start
                self.start_monitoring()

            logger.info(f"Necesse server '{self.world_name}' started on port {self.port} (UDP)")
            logger.info(f"Players can connect to: <your_ip>:{self.port}")
            if self.server_password:
                logger.info(f"Server password: {self.server_password}")
            return True

        except Exception as e:
            logger.error(f"Error starting Necesse server: {e}")
            return False

    def stop(self) -> bool:
        """Stop the Necesse server gracefully"""
        if self.process and self.process.poll() is None:
            try:
                # Necesse responds to "quit" command on stdin
                logger.info("Sending quit command to Necesse server...")
                self.process.stdin.write("quit\n")
                self.process.stdin.flush()

                # Wait for graceful shutdown
                try:
                    self.process.wait(timeout=15)
                    logger.info("Necesse server stopped gracefully")
                except subprocess.TimeoutExpired:
                    logger.warning("Server did not respond to quit command, forcing termination...")
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.warning("Server did not terminate, killing process...")
                        self.process.kill()
                        self.process.wait()

                self.stop_monitoring()
                self.is_running = False
                self.pid = None
                return True

            except Exception as e:
                logger.error(f"Error stopping Necesse server: {e}")
                # Fall back to parent class stop method
                return super().stop()
        else:
            self.stop_monitoring()
            return True  # Already stopped

    def get_status(self) -> dict:
        """Get Necesse server status with additional info"""
        status = super().get_status()
        status['world_name'] = self.world_name
        status['has_password'] = bool(self.server_password)
        status['max_slots'] = self.max_slots
        status['protocol'] = 'UDP'
        return status