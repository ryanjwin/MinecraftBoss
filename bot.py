import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('coordinates.db')
cursor = conn.cursor()

# Create a table to store coordinates if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coordinates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        x REAL,
        y REAL,
        z REAL
    )
''')
conn.commit()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready.

    This function prints a message to the console indicating that the bot has logged in.
    """
    await bot.tree.sync()
    print(f'We have logged in as {bot.user.name}')
    return

@bot.tree.command(name='hello')
async def hello(interaction: discord.Interaction):
    """
    Say hello!

    This function sends a greeting message mentioning the user who invoked the command.
    """
    await interaction.response.send_message(f'Hello to you too!', 
                                                 ephemeral=True)
    return

@bot.tree.command(name='h')
async def help(interaction: discord.Interaction):
    """
    Command to display help information.

    This function sends a message containing information about available commands.
    """
    help_message = (
        "Here are the available commands:\n"
        "!hello - Greet the bot\n"
        "!savecoords description x y z - Save coordinates\n"
        "!coords - List all coordinates\n"
        "!coords \{query\} - List coordinates matching the description\n"
        "!removecoords \{query\} - Remove coordinates matching the description\n"
        "!h - Display this help message"
    )
    await interaction.response.send_message(help_message, ephemeral=True)
    return

@bot.tree.command(name='savecoords')
async def savecoords(interaction: discord.Interaction, description: str, x: float, y: float, z: float):
    """
    Save coordinates to the database. Include the description and the coordinates.

    Parameters:
    - description (str): Description of the coordinates.
    - x (float): X-coordinate.
    - y (float): Y-coordinate.
    - z (float): Z-coordinate.
    """
    try:
        cursor.execute('INSERT INTO coordinates (description, x, y, z) VALUES (?, ?, ?, ?)',
                   (description, x, y, z))
        conn.commit()
    except Exception as e:
        await interaction.response.send_message(f'Invalid coordinates. Please ensure that x, y, and z are valid numbers. No commas! \n/h for more info',
                                            ephemeral=True)
    await interaction.response.send_message(f'Coordinates saved: [Description: {description}, X: {x}, Y: {y}, Z: {z}]',
                                            ephemeral=True)
    return

@bot.tree.command(name='coords')
async def coords(interaction: discord.Interaction, *, query: str = None):
    """
    Command to list coordinates stored in the database. Can optionally use a query for specific coordinates.

    Parameters:
    - query (str): Optional query to filter coordinates by description.

    This function lists all coordinates or filters coordinates based on the provided query.
    """
    # No specific query.
    if not query:
        cursor.execute('SELECT * FROM coordinates')
        all_coords = cursor.fetchall()
        # If there are no coordinates in the database.
        if not all_coords:
            await interaction.response.send_messag('No coordinates found.')
            return
        # All coordinates.
        coords_list = '\n'.join(f"{coord[1]}: X={coord[2]}, Y={coord[3]}, Z={coord[4]}" for coord in all_coords)
        await interaction.response.send_message(f'List of coordinates:\n{coords_list}', ephemeral=True)
        return
    # There is a query.
    cursor.execute('SELECT * FROM coordinates WHERE description LIKE ?', ('%' + query + '%',))
    filtered_coords = cursor.fetchall()
    # Nothing found from the query.
    if not filtered_coords:
        await interaction.response.send_message(f'No coordinates found matching the description: {query}', ephemeral=True)
        return
    # Return the query.
    coords_list = '\n'.join(f"{coord[1]}: X={coord[2]}, Y={coord[3]}, Z={coord[4]}" for coord in filtered_coords)
    await interaction.response.send_message(f'List of coordinates matching the description "{query}":\n{coords_list}', ephemeral=True)
    return

@bot.tree.command(name='removecoords')
async def remove(interaction: discord.Interaction, *, query: str):
    """
    Command to remove coordinates. Must match an exact phrase.

    Parameters:
    - query (str): Query to identify coordinates for removal.

    This function removes coordinates based on the provided exact query.
    """
    # Remove coordinates from the database with an exact match
    cursor.execute('DELETE FROM coordinates WHERE description = ?', (query,))
    conn.commit()

    await interaction.response.send_message(f'Coordinates with the exact description "{query}" have been removed.', ephemeral=True)
    return

if __name__ == '__main__':
    try:
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')
        bot.run(TOKEN)
    finally:
        conn.close()