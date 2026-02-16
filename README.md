# Discord Game Server Bot

A Discord bot that allows you to manage game servers (Terraria, Minecraft, Factorio, Necesse) directly from Discord using slash commands.

## Features

- Start, stop, and restart game servers
- Monitor server status and resource usage
- View server information and statistics
- Support for multiple game types (Terraria, Minecraft, Factorio, Necesse, Palworld)
- Slash command interface for easy use

## Prerequisites

- Python 3.8 or higher
- Discord bot token (create one at [Discord Developer Portal](https://discord.com/developers/applications))
- Game server executables installed on your system
- macOS, Linux, or Windows (this project is designed for macOS/Mac Mini deployment)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a Discord bot and add it to your server
4. Update the `config/config.json` file with your bot token and game server paths

## Configuration

Edit `config/config.json` to set up your bot and game server paths:

```json
{
  "discord_token": "YOUR_BOT_TOKEN_HERE",
  "games": {
    "terraria": {
      "executable_path": "/path/to/terraria/server",
      "default_port": 7777,
      "default_world": "world.wld"
    },
    "minecraft": {
      "executable_path": "/path/to/minecraft/server.jar",
      "default_port": 25565,
      "memory": "2G"
    },
    "factorio": {
      "executable_path": "/path/to/factorio/bin/x64/factorio",
      "default_port": 34197,
      "server_settings": "/path/to/factorio/server-settings.json"
    },
    "necesse": {
      "server_dir": "/path/to/necesse/server",
      "executable_path": "/path/to/necesse/server/StartServer-nogui.sh",
      "default_port": 14159,
      "world_name": "MyWorld",
      "max_slots": 8,
      "server_password": "",
      "owner_name": "",
      "use_local_dir": true
    }
  }
}
```

## Game Server Setup

Before using the bot, you need to download and configure each game server. See the detailed setup guides:

- **Necesse (macOS)**: [server_managers/setup_docs/necesse_macos.md](server_managers/setup_docs/necesse_macos.md) - **Complete step-by-step guide**
- **Necesse (Windows)**: [server_managers/setup_docs/necesse.md](server_managers/setup_docs/necesse.md)
- Other games: Setup guides to be added

Each guide includes:
- How to download server files
- Initial server configuration
- Bot configuration steps
- Port forwarding setup
- Troubleshooting

**Important**: Follow the game-specific setup guide for your platform before trying to start servers through the bot.

## Running the Bot

1. Make sure you have updated the configuration with your bot token
2. Ensure you have set up at least one game server (see setup guides above)
3. Run the bot:

```bash
python bot.py
```

Or with environment variable:
```bash
export DISCORD_TOKEN="your_token_here"
python bot.py
```

4. The bot should connect to Discord and be ready to use

## Available Commands

- `/start_server <game> [server_name]` - Start a game server
- `/stop_server <server_name>` - Stop a game server
- `/restart_server <server_name>` - Restart a game server
- `/status [server_name]` - Get status of all servers or a specific server
- `/list_servers` - List available games and managed servers
- `/server_logs <server_name> [lines]` - View server logs (placeholder implementation)

## Supported Games

- Terraria
- Minecraft (Java Edition)
- Factorio
- Necesse
- Palworld

## Security Note

When adding the bot to your Discord server, make sure to give it appropriate permissions. The bot only requires permissions to read messages, send messages, and use slash commands.

## Troubleshooting

**Bot Issues**:
- If the bot fails to start, check that your Discord token is correct in the config file
- Ensure game server executables exist at the specified paths in the config
- Make sure required ports are not already in use
- Check that the bot has necessary permissions in your Discord server

**Game Server Issues**:
- See the game-specific setup documentation in `server_managers/setup_docs/`
- For Necesse on macOS: Check [necesse_macos.md](server_managers/setup_docs/necesse_macos.md) troubleshooting section
- Verify paths in `config.json` are absolute paths (not `~`)
- Ensure server startup scripts have execute permissions (`chmod +x`)

**Connection Issues**:
- Verify port forwarding is configured on your router
- Check firewall settings on the server host
- Use your public IP address for external connections
- Use local IP address for same-network connections

## License

This project is licensed under the MIT License.