# Necesse Dedicated Server Setup - macOS

This guide covers setting up a Necesse dedicated server on macOS (for Mac Mini deployment).

## Quick Start Checklist

Follow these steps in order:

1. ✅ Download Necesse server files
2. ✅ Run server once manually to create initial world
3. ✅ Update Discord bot configuration file with server paths
4. ✅ Configure port forwarding on router
5. ✅ Test server through Discord bot commands
6. ✅ Share connection info with players

## Prerequisites

- macOS system with internet connection
- Java 17 or newer (bundled JRE is included with server files)
- Network access and ability to configure port forwarding
- Discord bot installed in this repository

## Complete Setup Walkthrough

### Step 1: Download Server Files

**Option A: Direct Download (Recommended)**

1. Open Safari or your preferred browser
2. Visit: https://necessegame.com/server/
3. Download the latest macOS server zip file (e.g., `necesse-server-macos-1-1-1-21292486.zip`)
4. Open Terminal and extract the files:
   ```bash
   # Navigate to Downloads folder
   cd ~/Downloads

   # Create a directory for the server
   mkdir -p ~/necesse-server

   # Extract the zip file
   unzip necesse-server-macos-*.zip -d ~/necesse-server

   # Navigate to the server directory
   cd ~/necesse-server

   # Make the startup script executable
   chmod +x StartServer-nogui.sh
   ```

**Option B: SteamCMD (Alternative)**

1. Install SteamCMD (see: https://developer.valvesoftware.com/wiki/SteamCMD#macOS)
2. Run SteamCMD and download the server:
   ```bash
   ./steamcmd.sh
   login anonymous
   force_install_dir ~/necesse-server
   app_update 1169370 validate
   quit
   ```
3. Server files will be in: `~/Library/Application Support/Steam/steamapps/common/Necesse Dedicated Server/`

### Step 2: Initial Server Setup (Manual First Run)

Before using the Discord bot, you need to create a world by running the server once manually:

```bash
# Navigate to server directory
cd ~/necesse-server

# Run the server for first-time setup
./StartServer-nogui.sh
```

You will be prompted to configure:

1. **World name**: Enter a name (e.g., `MyWorld`)
   - **IMPORTANT**: Remember this name exactly - you'll need it for the bot config!
2. **Custom server options**: Type `y` and press Enter
3. **Host port**: Enter `14159` (default) and press Enter
4. **Player slots**: Enter a number between 1-250 (e.g., `8`)
5. **Server password**: Enter a password or leave blank for no password
6. **Custom spawn island**: Leave blank and press Enter (for random)
7. **Spawn seed**: Leave blank and press Enter (for random)
8. **Spawn guide house**: Type `y` or `n` and press Enter

Once the server starts, you'll see: `"Server is ready!"`

**Stop the server by typing**: `quit` and press Enter

### Step 3: Configure Discord Bot

Now that you have the server set up, you need to tell the Discord bot where to find it.

1. Open the bot's configuration file in a text editor:
   ```bash
   # Navigate to the bot directory
   cd /path/to/discord_game_bot

   # Open config file with TextEdit or your preferred editor
   open -a TextEdit config/config.json
   ```

2. Find the `"necesse"` section and update these fields:

   ```json
   "necesse": {
     "server_dir": "/Users/YOUR_USERNAME/necesse-server",
     "executable_path": "/Users/YOUR_USERNAME/necesse-server/StartServer-nogui.sh",
     "default_port": 14159,
     "world_name": "MyWorld",
     "max_slots": 8,
     "server_password": "",
     "owner_name": "",
     "use_local_dir": true
   }
   ```

   **Replace the following**:
   - `YOUR_USERNAME` → Your actual macOS username
   - `MyWorld` → The exact world name you entered in Step 2
   - `max_slots` → The number of player slots you configured
   - `server_password` → The password you set (if any)
   - `owner_name` → Your player name for auto-owner permissions (optional)

3. **To find your username**, run in Terminal:
   ```bash
   whoami
   ```

4. **Example with actual values**:
   ```json
   "necesse": {
     "server_dir": "/Users/john/necesse-server",
     "executable_path": "/Users/john/necesse-server/StartServer-nogui.sh",
     "default_port": 14159,
     "world_name": "JohnsWorld",
     "max_slots": 16,
     "server_password": "secret123",
     "owner_name": "JohnDoe",
     "use_local_dir": true
   }
   ```

5. Save the file and close the editor

### Step 4: Configure Network (Port Forwarding)

Necesse uses **UDP port 14159** by default. You need to set up port forwarding so players can connect from the internet.

**Find Your Mac Mini's Local IP Address**:
```bash
# Run this command in Terminal
ifconfig | grep "inet " | grep -v 127.0.0.1
```
Look for something like `192.168.1.XXX` or `10.0.0.XXX`

**Configure Your Router**:

1. Find your public IP address: https://whatismyipaddress.com/
2. Log into your router's admin panel (usually http://192.168.1.1 or http://10.0.0.1)
3. Find "Port Forwarding" or "Virtual Server" settings
4. Create a new port forward rule:
   - **Service Name**: Necesse Server
   - **Protocol**: UDP
   - **External Port**: 14159
   - **Internal Port**: 14159
   - **Internal IP**: Your Mac Mini's IP (from command above)
   - **Enable**: Yes/On

5. Save the settings

**Configure macOS Firewall** (if enabled):

1. Open **System Settings** → **Network** → **Firewall**
2. If firewall is enabled:
   - Click **Options**
   - Click **+** to add a new rule
   - Navigate to your necesse-server folder and select `StartServer-nogui.sh` or the Java process
   - Set to "Allow incoming connections"
3. Alternative: Disable firewall temporarily for testing (re-enable after confirming it works)

**Test Your Port Forwarding**:

1. Start the server (see Step 5)
2. Visit: https://portchecker.co/
3. Enter your public IP and port `14159`
4. Select UDP protocol
5. Click "Check"

**Note**: Some port checkers show false negatives for UDP. If configured correctly but shows as closed, have a friend test connecting to verify.

### Step 5: Test with Discord Bot

Now you're ready to test the server through the Discord bot!

**Start the Discord Bot**:
```bash
# Navigate to bot directory
cd /path/to/discord_game_bot

# Make sure you have your Discord token set
export DISCORD_TOKEN="your_token_here"

# Or add it to config/config.json

# Run the bot
python3 bot.py
```

**Discord Commands to Test**:

1. **Start the server**:
   ```
   /start_server game:necesse
   ```
   You should see: "Necesse server 'necesse' started successfully!"

2. **Check server status**:
   ```
   /status server_name:necesse
   ```
   Should show:
   - Running: Yes
   - Port: 14159
   - World name: (your world name)
   - etc.

3. **View all servers**:
   ```
   /list_servers
   ```

4. **Stop the server** (when done testing):
   ```
   /stop_server server_name:necesse
   ```

### Step 6: Share Connection Info with Players

Once the server is running, give players this information:

**Connection Details**:
- **IP Address**: Your public IP from https://whatismyipaddress.com/
- **Port**: 14159
- **Password**: (if you set one)

**How Players Connect**:

1. Launch Necesse from Steam
2. Click **Multiplayer**
3. Click **Add Server**
4. Fill in:
   - **Name**: Any friendly name
   - **IP Address**: Your public IP (e.g., `123.45.67.89`)
   - **Port Number**: `14159`
5. Click **Add**
6. Double-click the server to join
7. Enter password if prompted

**Local Network Players**: If connecting from the same network as the Mac Mini, use the local IP (192.168.x.x) instead of the public IP.

---

## Reference Documentation

The sections below provide additional technical details and reference information.

### Configuration Files and Locations

When using `-localdir` (default in bot config):
- **Server config**: `~/necesse-server/cfg/server.cfg`
- **World saves**: `~/necesse-server/saves/`
- **Logs**: `~/necesse-server/logs/`

When NOT using `-localdir`:
- **Server config**: `~/.config/Necesse/cfg/server.cfg`
- **World saves**: `~/.config/Necesse/saves/`
- **Logs**: `~/.config/Necesse/logs/`

### Manual Server Control (Advanced)

You can run the server manually without the Discord bot if needed:

**Start server interactively** (for initial setup):
```bash
cd ~/necesse-server
./StartServer-nogui.sh
```

**Start server non-interactively** (with existing world):
```bash
cd ~/necesse-server
./StartServer-nogui.sh -world YourWorldName
```

**Full command with all parameters**:
```bash
./StartServer-nogui.sh \
  -world MyWorld \
  -port 14159 \
  -slots 8 \
  -password "your_password" \
  -owner "YourPlayerName" \
  -localdir \
  -pausewhenempty 1 \
  -logging 1
```

**Note**: When using the Discord bot, you don't need to run these commands manually. The bot handles starting/stopping automatically.

### Server Parameters Reference

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-world <name>` | World to load (required for non-interactive) | `-world SaveGame1` |
| `-port <port>` | Server port (default: 14159) | `-port 14159` |
| `-slots <number>` | Max players (1-250) | `-slots 16` |
| `-password <pass>` | Server password (blank for none) | `-password secret123` |
| `-owner <name>` | Auto-assign owner permissions | `-owner AdminName` |
| `-localdir` | Use local directory for data | `-localdir` |
| `-datadir <path>` | Custom data directory | `-datadir /path/to/data` |
| `-pausewhenempty <0\|1>` | Pause when no players (default 0) | `-pausewhenempty 1` |
| `-logging <0\|1>` | Enable logging (default 1) | `-logging 1` |
| `-motd <message>` | Message of the day (use \\n for newlines) | `-motd "Welcome!"` |
| `-giveclientspower <0\|1>` | Anti-cheat (off = smoother, default 0) | `-giveclientspower 0` |

### Stopping the Server Manually

**If running manually** (not through Discord bot):

Graceful shutdown - type in the console:
```
quit
```

Force stop if unresponsive:
```bash
# Find the process
ps aux | grep necesse

# Kill it (replace PID with actual process ID)
kill <PID>
```

**If running through Discord bot**, use:
```
/stop_server server_name:necesse
```

## Troubleshooting

### Discord Bot Can't Start Server

**Error**: "Necesse server startup script not found"

**Solution**:
1. Verify the path in `config/config.json` is correct
2. Check that the file exists:
   ```bash
   ls -la /Users/YOUR_USERNAME/necesse-server/StartServer-nogui.sh
   ```
3. Make sure you're using absolute paths, not `~` in config.json
4. Ensure the script is executable:
   ```bash
   chmod +x /Users/YOUR_USERNAME/necesse-server/StartServer-nogui.sh
   ```

**Error**: "World not found" or server asks for setup interactively

**Solution**:
1. Make sure you ran the server manually first (Step 2)
2. Verify the `world_name` in config.json matches EXACTLY (case-sensitive)
3. Check that the world exists:
   ```bash
   # If using -localdir
   ls ~/necesse-server/saves/

   # If NOT using -localdir
   ls ~/.config/Necesse/saves/
   ```

### Server Won't Start Manually

**Issue**: Permission denied when running `./StartServer-nogui.sh`

**Solution**:
```bash
chmod +x ~/necesse-server/StartServer-nogui.sh
```

**Issue**: "Java not found" error

**Solution**:
The server includes bundled Java, but if you see this error:
```bash
# Check if Java is installed
java -version

# If not, install Java 17:
brew install openjdk@17
```

**Issue**: Script runs but exits immediately

**Solution**: Check the logs:
```bash
# If using -localdir
cat ~/necesse-server/logs/latest.log

# If NOT using -localdir
cat ~/.config/Necesse/logs/latest.log
```

### Players Can't Connect to Server

**Issue**: "Connection failed" or "Server not responding"

**Solutions**:
1. **Verify server is running**:
   ```bash
   ps aux | grep necesse
   ```
   Should show the server process

2. **Check you gave them the correct IP**:
   - Use PUBLIC IP for internet players: https://whatismyipaddress.com/
   - Use LOCAL IP for same-network players: `ifconfig | grep "inet "`

3. **Verify port forwarding**:
   - Router must forward UDP port 14159 to Mac Mini's local IP
   - Test at: https://portchecker.co/

4. **Check macOS firewall**:
   - System Settings → Network → Firewall
   - Ensure Necesse/Java is allowed, or disable firewall temporarily

5. **Verify correct port**:
   - Default is 14159
   - Check `config.json` to confirm what port you configured
   - Tell players to use that port

**Issue**: Port checker shows port closed but server is running

**Solution**:
- UDP ports often show false negatives on port checkers
- Have a friend try to actually connect - this is the real test
- If they can connect, port forwarding is working correctly

### Server Performance Issues

**Issue**: Server is laggy or crashes

**Solutions**:
1. Check available resources:
   - Open Activity Monitor
   - Look for Necesse or Java process
   - Check CPU and memory usage

2. Reduce player slots in `config.json`:
   ```json
   "max_slots": 4
   ```

3. Check disk space:
   ```bash
   df -h
   ```

4. Review server logs for errors:
   ```bash
   tail -f ~/necesse-server/logs/latest.log
   ```

### Wrong World Loads or World Not Found

**Issue**: Server loads wrong world or says world doesn't exist

**Solutions**:
1. World names are CASE-SENSITIVE: `MyWorld` ≠ `myworld`

2. Check exact world name:
   ```bash
   # If using -localdir (default with bot)
   ls ~/necesse-server/saves/

   # World files are named: WorldName.zip
   # Use "WorldName" in config (without .zip)
   ```

3. Verify you're consistent with `-localdir`:
   - Bot config has `"use_local_dir": true` → worlds in `~/necesse-server/saves/`
   - If set to `false` → worlds in `~/.config/Necesse/saves/`

4. If world exists but won't load, try deleting world cache:
   ```bash
   rm -rf ~/necesse-server/cache/
   # Or
   rm -rf ~/.config/Necesse/cache/
   ```

### Discord Bot Issues

**Issue**: Bot doesn't respond to commands

**Solution**:
1. Check bot is running:
   ```bash
   ps aux | grep "python.*bot.py"
   ```

2. Check bot logs for errors

3. Verify Discord token is set

4. Make sure bot has synced slash commands (wait a minute after bot starts)

**Issue**: Bot shows server as stopped but it's running

**Solution**:
1. Stop the server manually:
   ```bash
   ps aux | grep necesse
   kill <PID>
   ```

2. Start it through the bot:
   ```
   /start_server game:necesse
   ```

This ensures the bot tracks the process correctly.

## Server Commands

Once connected to the server, you can use these commands (as owner):

| Command | Description |
|---------|-------------|
| `/help` | List all commands |
| `/save` | Save the world |
| `/stop` | Stop the server |
| `/password <pass>` | Change server password |
| `/permissions set <player> <level>` | Set player permissions |
| `/motd <message>` | Set message of the day |

Full command reference: https://necessewiki.com/Multiplayer#Server_and_chat_commands

## Updating the Server

### Direct Download Method
1. Download latest macOS server zip from https://necessegame.com/server/
2. Stop the running server
3. Extract new files to server directory (this updates the executable)
4. Start the server (world saves are separate and won't be affected)

### SteamCMD Method
```bash
./steamcmd.sh
login anonymous
force_install_dir ~/necesse-server
app_update 1169370 validate
quit
```

**Note**: Always backup your world saves before updating!

## Quick Reference

### Essential Commands

**Start server through Discord bot**:
```
/start_server game:necesse
```

**Stop server through Discord bot**:
```
/stop_server server_name:necesse
```

**Check server status**:
```
/status server_name:necesse
```

**Get your Mac Mini's local IP**:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Get your public IP**:
Visit: https://whatismyipaddress.com/

**View server logs**:
```bash
# If using -localdir (default)
tail -f ~/necesse-server/logs/latest.log

# If NOT using -localdir
tail -f ~/.config/Necesse/logs/latest.log
```

**Check if server is running**:
```bash
ps aux | grep necesse
```

### Important Files

**Bot configuration**:
```
discord_game_bot/config/config.json
```

**Server directory** (typical installation):
```
~/necesse-server/
```

**World saves** (with -localdir):
```
~/necesse-server/saves/
```

**Server config** (with -localdir):
```
~/necesse-server/cfg/server.cfg
```

### Default Settings

- **Port**: 14159 (UDP)
- **Max Players**: 8 (configurable)
- **Default World Location**: `~/necesse-server/saves/` (with `-localdir`)

### Connection Info to Share

Give players:
1. **IP**: Your public IP from https://whatismyipaddress.com/
2. **Port**: 14159
3. **Password**: (if you set one)

### Common Config Values

Example `config.json` entry:
```json
"necesse": {
  "server_dir": "/Users/john/necesse-server",
  "executable_path": "/Users/john/necesse-server/StartServer-nogui.sh",
  "default_port": 14159,
  "world_name": "MyWorld",
  "max_slots": 8,
  "server_password": "",
  "owner_name": "AdminName",
  "use_local_dir": true
}
```

## Additional Resources

- **Official Wiki**: https://necessewiki.com/Multiplayer
- **Linux Setup Guide** (similar to macOS): https://necessewiki.com/Multiplayer-Linux
- **Server Downloads**: https://necessegame.com/server/
- **Steam App ID**: 1169370
- **Port Checker**: https://portchecker.co/
- **What's My IP**: https://whatismyipaddress.com/
