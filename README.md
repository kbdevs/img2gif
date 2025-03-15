# Discord PNG to GIF Bot

A Discord bot that converts images to single-frame GIFs, with support for user-installable commands.

## Features

- Slash command `/togif` that converts an attached image to a single-frame GIF
- Context menu command "Convert to GIF" when right-clicking on messages with images
- User-installable command that can be used in any server or DM
- All responses are ephemeral (only visible to the user who triggered the command)
- Supports PNG, JPG, JPEG, WEBP, and BMP image formats

## Setup

1. Make sure you have Python 3.8 or higher installed

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Note: This will install the master branch of discord.py which is required for user-installable commands.

3. Run the bot:
   ```
   python script.py
   ```

## Usage

### For Bot Owners

1. Register your application in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable the "Message Content Intent" in the Bot section
3. In the OAuth2 URL Generator:
   - Select scopes: `bot`, `applications.commands`
   - Select bot permissions: `Send Messages`, `Attach Files`, `Use Slash Commands`
4. Use the generated URL to invite the bot to your server

### For Users

1. Users can install the command to their account by:
   - Right-clicking on the bot in a server
   - Selecting "Add to Home"
   - Following the prompts to install the command

2. Once installed, users can use the bot in two ways:
   - **Slash Command**: Type `/togif` and attach an image when prompted
   - **Context Menu**: Right-click on any message containing an image and select "Apps" > "Convert to GIF"

3. The bot will convert the image to a GIF and send it back without any accompanying text. All responses are ephemeral (only visible to you).

## Security Note

The bot token in the script should be kept private. For production use, consider using environment variables to store sensitive information.

## Troubleshooting

- If the bot doesn't respond, make sure it has the necessary permissions in the channel
- For large images, the conversion might take a moment
- If you encounter any errors, they will be displayed in the Discord channel
- If commands aren't showing up for users, make sure you're using the master branch of discord.py and have synced the command tree

### DM Usage Issues

If the command doesn't appear in DMs after installation:

1. **Restart Discord**: Sometimes Discord needs a restart to show newly installed commands in DMs.

2. **Check Installation**: Make sure you've properly installed the command to your user account:
   - Right-click on the bot in a server
   - Select "Add to Home"
   - Confirm the installation

3. **Bot Requirements**: The bot must be using the master branch of discord.py (2.3.2 or newer) and have the `@app_commands.allowed_contexts(dms=True)` decorator.

4. **Reinstall**: Try removing the bot from your Home and reinstalling it.

5. **Discord Limitations**: There might be rate limits or other Discord-side limitations affecting command availability. 