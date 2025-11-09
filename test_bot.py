#!/usr/bin/env python3
"""
Test script to demonstrate the game server bot functionality
This script shows how the server management system works without running the full Discord bot
"""

import sys
import os
import time
import json
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from server_managers.base_server import ServerManager

def load_test_config():
    """Load a test configuration"""
    return {
        "games": {
            "terraria": {
                "executable_path": "/mock/path/terraria/server",
                "default_port": 7777,
                "default_world": "world.wld"
            },
            "minecraft": {
                "executable_path": "/mock/path/minecraft/server.jar",
                "default_port": 25565,
                "memory": "2G"
            },
            "factorio": {
                "executable_path": "/mock/path/factorio/bin/x64/factorio",
                "default_port": 34197,
                "server_settings": "/mock/path/factorio/server-settings.json"
            },
            "necesse": {
                "executable_path": "/mock/path/necesse/server.jar",
                "default_port": 42780,
                "memory": "2G"
            }
        }
    }

def test_server_management():
    """Test the server management functionality"""
    print("Testing Game Server Management System")
    print("=" * 50)
    
    # Create server manager with test config
    config = load_test_config()
    server_manager = ServerManager(config)
    
    print(f"Available games: {', '.join(server_manager.get_available_games())}")
    print(f"Managed servers: {server_manager.list_servers()}")
    
    # Create a test server (Terraria)
    print("\nCreating Terraria server...")
    terraria_server = server_manager.create_server("terraria", "test-terraria")
    if terraria_server:
        print(f"✓ Created server: {terraria_server.name}")
    
    # Create a Minecraft server
    print("\nCreating Minecraft server...")
    minecraft_server = server_manager.create_server("minecraft", "test-minecraft")
    if minecraft_server:
        print(f"✓ Created server: {minecraft_server.name}")
    
    print(f"Managed servers: {server_manager.list_servers()}")
    
    # Show statuses (they won't be running since we're using mock paths)
    print("\nServer statuses:")
    statuses = server_manager.get_status()
    for name, status in statuses.items():
        print(f"  {name}: Running={status['running']}, Port={status['port']}, PID={status['pid']}")
    
    print("\nTest completed successfully!")
    print("\nNote: In a real environment, the bot would attempt to start actual server processes")
    print("using the executable paths specified in the config file.")

if __name__ == "__main__":
    test_server_management()