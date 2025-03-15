import discord
from discord import app_commands
import os
import io
from PIL import Image
import aiohttp

# Set up the client with intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'Bot is ready! Logged in as {client.user}')
    
    # Sync the command tree with Discord globally
    try:
        # This syncs commands globally
        await tree.sync()
        print("Command tree synced globally!")
    except Exception as e:
        print(f"Failed to sync command tree: {e}")

# Function to convert image to GIF
async def convert_image_to_gif(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    
    # Create a BytesIO object to save the GIF
    gif_bytes = io.BytesIO()
    
    # Save as GIF with a single frame
    img.save(gif_bytes, format='GIF', save_all=True, append_images=[], duration=0, loop=0)
    gif_bytes.seek(0)
    
    return gif_bytes

@tree.command(name="togif", description="Convert an image to a single-frame GIF")
@app_commands.user_install()  # Make the command user-installable
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # Allow it to be used anywhere
@app_commands.describe(image="The image to convert to a GIF")
async def to_gif(interaction: discord.Interaction, image: discord.Attachment):
    """Convert an attached image to a single-frame GIF"""
    # Check if the attachment is an image
    if not any(image.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp']):
        await interaction.response.send_message("Please attach a valid image file (PNG, JPG, JPEG, WEBP, BMP)!", ephemeral=True)
        return
    
    # Defer the response since image processing might take time
    await interaction.response.defer(thinking=True, ephemeral=True)
    
    try:
        # Download the image
        image_bytes = await image.read()
        gif_bytes = await convert_image_to_gif(image_bytes)
        
        # Send the GIF back
        await interaction.followup.send(
            file=discord.File(fp=gif_bytes, filename=f"{os.path.splitext(image.filename)[0]}.gif"),
            ephemeral=True
        )
        
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

# Add a context menu command for messages
@tree.context_menu(name="Convert to GIF")
@app_commands.user_install()  # Make the command user-installable
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # Allow it to be used anywhere
async def convert_to_gif(interaction: discord.Interaction, message: discord.Message):
    """Convert an image in a message to a single-frame GIF"""
    # Check if the message has attachments
    if not message.attachments:
        await interaction.response.send_message("This message doesn't contain any images to convert!", ephemeral=True)
        return
    
    # Find the first valid image attachment
    valid_image = None
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp']):
            valid_image = attachment
            break
    
    if not valid_image:
        await interaction.response.send_message("No valid image found in this message. Supported formats: PNG, JPG, JPEG, WEBP, BMP", ephemeral=True)
        return
    
    # Defer the response since image processing might take time
    await interaction.response.defer(thinking=True, ephemeral=True)
    
    try:
        # Download the image
        image_bytes = await valid_image.read()
        gif_bytes = await convert_image_to_gif(image_bytes)
        
        # Send the GIF back
        await interaction.followup.send(
            file=discord.File(fp=gif_bytes, filename=f"{os.path.splitext(valid_image.filename)[0]}.gif"),
            ephemeral=True
        )
        
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

# Run the bot with your token
client.run('')  # Your bot token
