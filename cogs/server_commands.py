import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger('GameServerBot')

class ServerCommandsCog(commands.Cog, name="Server Commands"):
    """Commands for managing game servers"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="start_server", description="Start a game server")
    @app_commands.describe(
        game="The game server to start",
        server_name="Optional custom name for the server instance"
    )
    async def start_server(self, interaction: discord.Interaction, game: str, server_name: str = None):
        """Start a game server"""
        await interaction.response.defer(thinking=True)
        
        # If server_name is not provided, use the game name
        if server_name is None:
            server_name = game.lower()
        
        # Check if the specified game is supported
        available_games = self.bot.server_manager.get_available_games()
        if game.lower() not in available_games:
            await interaction.followup.send(
                f"Game '{game}' is not supported. Available games: {', '.join(available_games)}"
            )
            return
        
        # Create server if it doesn't exist
        server = self.bot.server_manager.get_server(server_name)
        if not server:
            server = self.bot.server_manager.create_server(game.lower(), server_name)
            if not server:
                await interaction.followup.send(f"Failed to create {game} server")
                return
        
        # Start the server
        success = self.bot.server_manager.start_server(server_name)
        if success:
            await interaction.followup.send(f"{game.capitalize()} server '{server_name}' started successfully!")
        else:
            await interaction.followup.send(f"Failed to start {game} server '{server_name}'. It might already be running.")
    
    @app_commands.command(name="stop_server", description="Stop a game server")
    @app_commands.describe(server_name="The name of the server to stop")
    async def stop_server(self, interaction: discord.Interaction, server_name: str):
        """Stop a game server"""
        await interaction.response.defer(thinking=True)
        
        success = self.bot.server_manager.stop_server(server_name)
        if success:
            await interaction.followup.send(f"Server '{server_name}' stopped successfully!")
        else:
            await interaction.followup.send(f"Failed to stop server '{server_name}'. It might not be running or doesn't exist.")
    
    @app_commands.command(name="restart_server", description="Restart a game server")
    @app_commands.describe(server_name="The name of the server to restart")
    async def restart_server(self, interaction: discord.Interaction, server_name: str):
        """Restart a game server"""
        await interaction.response.defer(thinking=True)
        
        success = self.bot.server_manager.restart_server(server_name)
        if success:
            await interaction.followup.send(f"Server '{server_name}' restarted successfully!")
        else:
            await interaction.followup.send(f"Failed to restart server '{server_name}'.")
    
    @app_commands.command(name="status", description="Get status of all game servers or a specific server")
    @app_commands.describe(server_name="Optional specific server to check")
    async def status(self, interaction: discord.Interaction, server_name: str = None):
        """Get status of game servers"""
        await interaction.response.defer(thinking=True)
        
        if server_name:
            status = self.bot.server_manager.get_status(server_name)
            if 'error' in status:
                await interaction.followup.send(status['error'])
                return
            
            embed = discord.Embed(
                title=f"Server Status: {status['name']}",
                color=discord.Color.green() if status['running'] else discord.Color.red()
            )
            embed.add_field(name="Running", value="Yes" if status['running'] else "No", inline=True)
            embed.add_field(name="PID", value=status['pid'] or "N/A", inline=True)
            embed.add_field(name="Port", value=status['port'], inline=True)
            
            # Add monitoring data if available
            monitoring_data = status.get('monitoring_data')
            if monitoring_data:
                cpu_usage = monitoring_data.get('cpu_percent', 0)
                mem_usage = monitoring_data.get('memory_percent', 0)
                
                embed.add_field(name="CPU Usage", value=f"{cpu_usage:.1f}%", inline=True)
                embed.add_field(name="Memory Usage", value=f"{mem_usage:.1f}%", inline=True)
            
            await interaction.followup.send(embed=embed)
        else:
            statuses = self.bot.server_manager.get_status()
            if not statuses:
                await interaction.followup.send("No servers are currently managed by the bot.")
                return
            
            embed = discord.Embed(title="Server Status", color=discord.Color.blue())
            
            for name, status in statuses.items():
                server_status = "✅ Running" if status['running'] else "❌ Stopped"
                
                # Build server info string
                server_info = f"Status: {server_status}\nPort: {status['port']}\nPID: {status['pid'] or 'N/A'}"
                
                # Add monitoring data if available
                monitoring_data = status.get('monitoring_data')
                if monitoring_data:
                    cpu_usage = monitoring_data.get('cpu_percent', 0)
                    mem_usage = monitoring_data.get('memory_percent', 0)
                    server_info += f"\nCPU: {cpu_usage:.1f}% | Memory: {mem_usage:.1f}%"
                
                embed.add_field(
                    name=name,
                    value=server_info,
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="list_servers", description="List all available games and managed servers")
    async def list_servers(self, interaction: discord.Interaction):
        """List all available games and managed servers"""
        await interaction.response.defer(thinking=True)
        
        available_games = self.bot.server_manager.get_available_games()
        managed_servers = self.bot.server_manager.list_servers()
        
        embed = discord.Embed(title="Game Server Management", color=discord.Color.gold())
        
        embed.add_field(
            name="Available Games",
            value="\n".join([f"• {game.capitalize()}" for game in available_games]) or "None",
            inline=False
        )
        
        embed.add_field(
            name="Managed Servers",
            value="\n".join([f"• {server}" for server in managed_servers]) or "None",
            inline=False
        )
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="server_logs", description="View recent logs from a server")
    @app_commands.describe(server_name="The server to view logs for", lines="Number of lines to show (default 10)")
    async def server_logs(self, interaction: discord.Interaction, server_name: str, lines: int = 10):
        """View recent logs from a server"""
        await interaction.response.defer(thinking=True)
        
        # For now, we'll just show that logs aren't implemented yet
        # In a real implementation, we'd have a way to collect logs from the servers
        await interaction.followup.send(f"Server logs for '{server_name}' are not yet implemented. This would show the last {lines} lines from the server's logs.")

# Set up the cog
async def setup(bot):
    await bot.add_cog(ServerCommandsCog(bot))