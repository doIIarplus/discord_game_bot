This file provides a set of basic behavioural patterns and rules for Claude when parsing this project. Claude should remember the existence of this file during operation.

Claude is free to create and modify any markdown files prefixed with `claude` (E.G. `claude_necesse.md`) to assist in context compression and parsing. Other files should be asked about as normal.

Claude should remember that the hardware user will not have access to the software coding context/history. So any instructions for setup should be stored in the corresponding markdown file.

Claude is free to restructure additional directories for each game depending on need.

Claude should remember to divide work into 2 parts unless stated otherwise. First it should work on the game specific server scripts, then it should only consider changes to the bot itself after those are finalized.

Claude should remember this repo will be run on a Mac Mini, as steps for server hosting may differ greatly between different OS.

# Context

This repo contains a Discord bot for controlling a hardware device for hosting game servers. It should be using dedicated server hosting scripts so it does not need to spend compute power to run the game itself.

Instructions for the server setup (usually taken from the wiki of each game), should be in the `./server_managers/setup_docs`. Claude should remember that not all instructions are for MacOS, so we may have to explore the equivalencies.

Each doc will contain unique setup instructions for each game. A few downloads and manual setup actions when adding a new game is acceptable and is considered out-of-scope. This project wants to automate anything repetitive with launching a server. The setup files should be modified for clarity on steps if necessary.

- The bot takes in commands to launch a server

- Each server's process should be distinguishable for shutdown commands

- The necessary server information for connecting (ip/password/etc.) should be returned back to the Discord bot for eventual display to users

Claude should not assume any format for server setup. Some may require `.jar`, some may require python, some may have a dedicated server executable on Steam to be launched VIA script instead.

# Additional Context
