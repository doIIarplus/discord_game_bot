import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GameServerBot')

class GameServerBot(commands.Bot):
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        
        # Initialize intents
        intents = discord.Intents.default()
        intents.message_content = True  # Required for processing messages if needed
        intents.guilds = True
        intents.guild_messages = True
        
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=None  # Disable default help command since we'll use slash commands
        )
        
        # Server management will be initialized after bot is ready
        self.server_manager = None

    def load_config(self):
        """Load configuration from config.json file"""
        config_path = Path(__file__).parent / 'config' / 'config.json'
        
        if not config_path.exists():
            logger.error(f"Config file not found at {config_path}")
            return {}
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    async def setup_hook(self):
        """This is called when the bot is ready to set up slash commands"""
        # Load all cogs
        await self.load_extension('cogs.server_commands')
        
        # Sync slash commands
        await self.tree.sync()
        logger.info("Slash commands synced")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guild(s)')
        
        # Initialize server manager after bot is ready
        from server_managers.base_server import ServerManager
        self.server_manager = ServerManager(self.config)
        
        logger.info("GameServerBot is ready!")

def main():
    # Create and run the bot
    token = os.getenv('DISCORD_TOKEN') or GameServerBot().config.get('discord_token')
    
    if not token or token == 'YOUR_BOT_TOKEN_HERE':
        logger.error("No Discord token found! Please set DISCORD_TOKEN environment variable or update config.json")
        return
    
    bot = GameServerBot()
    
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == '__main__':
    main()