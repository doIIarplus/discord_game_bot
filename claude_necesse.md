# Necesse Server Implementation - Context & Issues

## Current State Analysis

### Issues Found in Current Implementation

1. **Incorrect Port Configuration**
   - Config shows: `42780`
   - Actual default port per docs: `14159` (UDP protocol)

2. **Wrong Server Execution Method**
   - Current code tries to run as: `java -jar necesse.jar -port X -maxPlayers Y`
   - According to setup docs, Necesse uses:
     - `StartServer.bat` for Windows
     - `Necesse.jar` with specific parameters
     - Server can be run with `-nogui` for headless operation
     - Uses config files (`server.cfg`) instead of all CLI args

3. **Platform Considerations**
   - Setup docs are Windows-focused (`StartServer.bat`, paths like `C:\Users\...`)
   - Project mentions Mac Mini in claude.md
   - Current development environment: Windows 11 Pro
   - Need to determine target platform

4. **Server Configuration**
   - First-time setup is interactive (world name, port, slots, password, etc.)
   - Subsequent runs can use `-world` parameter to load existing world
   - Config stored in `%appdata%\Necesse\cfg\server.cfg`
   - Can force local config with `-localdir` parameter

5. **Missing Parameters from Docs**
   - `-nogui` - Run in terminal without GUI
   - `-world <name>` - Load specific world
   - `-port <port>` - Server port (default 14159)
   - `-slots <slots>` - Player slots (1-250)
   - `-owner <name>` - Auto-assign owner permissions
   - `-password <password>` - Server password
   - `-pausewhenempty <1/0>` - Pause when no players
   - `-localdir` - Use local directory for configs/saves

## Next Steps to Fix

### Phase 1: Server Scripts (necesse_server.py)

1. **Update port configuration**
   - Change default_port from 42780 to 14159
   - Document UDP protocol requirement

2. **Fix server startup logic**
   - Determine if server files are installed
   - Check for existing world/config
   - Build proper command with correct parameters
   - Support both Windows (.bat) and macOS/Linux execution

3. **Add configuration management**
   - Support `-localdir` for project-local server data
   - Pre-configure server.cfg to avoid interactive prompts
   - Allow custom world names, passwords, etc.

4. **Improve process management**
   - Handle graceful shutdown (server responds to "quit" command)
   - Capture server output for status/logs
   - Detect when server is actually ready vs just started

### Phase 2: Bot Changes (if needed)

- Consider after server scripts are finalized
- May need additional Discord commands for Necesse-specific features
- Could add world management commands

## macOS/Linux Server Information (from Wiki)

### Installation Methods

1. **Direct Download** (Recommended for Mac Mini)
   - Download from: https://necessegame.com/server/
   - macOS zip: `necesse-server-macos-<version>.zip`
   - Extract and run `StartServer-nogui.sh`

2. **SteamCMD** (Alternative)
   - App ID: `1169370`
   - Installs to: `~/Steam/steamapps/common/Necesse Dedicated Server/`

### Startup Commands

**Interactive (first-time setup):**
```bash
./StartServer-nogui.sh
```

**Non-interactive (with existing world):**
```bash
./StartServer-nogui.sh -world <WorldName>
```

### Server Parameters (Unix)

All same as Windows, including:
- `-nogui` - Run without GUI (already in script name for Unix)
- `-world <name>` - Load specific world
- `-port <port>` - Server port (default 14159)
- `-slots <slots>` - Player slots
- `-password <password>` - Server password
- `-localdir` - Use launch directory for saves/config
- `-datadir <path>` - Custom data directory

### File Locations (macOS/Linux)

**Default:**
- Config: `~/.config/Necesse/cfg/server.cfg`
- Saves: `~/.config/Necesse/saves/`
- Logs: `~/.config/Necesse/logs/`

**With `-localdir`:**
- Everything stored in server installation directory

### Java Requirement

- Bundled JRE included in server files
- Compatible with Java 17 if using external Java

## Implementation Plan for Mac Mini

### Phase 1: Update necesse_server.py

1. **Fix configuration**
   - Change port from 42780 to 14159
   - Add server installation path configuration
   - Add world name configuration
   - Consider using `-localdir` for easier management

2. **Update startup logic**
   - Look for `StartServer-nogui.sh` script
   - Build command: `./StartServer-nogui.sh -world <name> -port 14159 [other params]`
   - Handle first-time setup vs existing world
   - Set working directory to server installation folder

3. **Improve shutdown**
   - Server responds to "quit" command on stdin
   - Can also use graceful termination signals

4. **Add configuration options**
   - World name
   - Server password (optional)
   - Max players
   - Owner name (for auto-permissions)
   - Use local directory vs system directory

### Phase 2: Update config.json

1. Fix port to 14159
2. Update executable_path to point to `StartServer-nogui.sh`
3. Add world_name, server_password, max_slots, owner_name

### Phase 3: Update setup docs

1. Create macOS-specific setup instructions
2. Keep Windows docs for reference
3. Document where to download macOS server files
