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

@bot.hybrid_command(name='hello')
async def hello(ctx):
    """
    Command to greet the bot.

    Parameters:
    - ctx (Context): The context of the command.

    This function sends a greeting message mentioning the user who invoked the command.
    """
    await ctx.send(f'Hello to you too! {ctx.author.mention}')
    return

@bot.hybrid_command(name='h')
async def help(ctx):
    """
    Command to display help information.

    Parameters:
    - ctx (Context): The context of the command.

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
    await ctx.send(help_message)
    return

@bot.hybrid_command(name='savecoords')
async def savecoords(ctx, description: str, x: float, y: float, z: float):
    """
    Save coordinates to the database.

    Parameters:
    - description (str): Description of the coordinates.
    - x (float): X-coordinate.
    - y (float): Y-coordinate.
    - z (float): Z-coordinate.
    """
    if not args or len(args) < 4:
        await ctx.send('Please provide the description, x, y, and z coordinates. \n!h for more info')
        return
    
    # # Parse the arguments
    # description = ' '.join(args[:-3])
    # x = args[-3]
    # y = args[-2]
    # z = args[-1]

    # # Verify that x, y, and z are floats
    # try:
    #     x = float(x)
    #     y = float(y)
    #     z = float(z)
    # except ValueError:
    #     await ctx.send('Invalid coordinates. Please ensure that x, y, and z are valid numbers. No commas! \n!h for more info')
    #     return

    # insert into database
    # Insert into the database
    cursor.execute('INSERT INTO coordinates (description, x, y, z) VALUES (?, ?, ?, ?)',
                   (description, x, y, z))
    conn.commit()

    await ctx.send(f'Coordinates saved: [Description: {description}, X: {x}, Y: {y}, Z: {z}]')
    return

@bot.hybrid_command(name='coords')
async def coords(ctx, *, query = None):
    """
    Command to list coordinates.

    Parameters:
    - ctx (Context): The context of the command.
    - query (str): Optional query to filter coordinates by description.

    This function lists all coordinates or filters coordinates based on the provided query.
    """
    # No specific query.
    if not query:
        cursor.execute('SELECT * FROM coordinates')
        all_coords = cursor.fetchall()
        # If there are no coordinates in the database.
        if not all_coords:
            await ctx.send('No coordinates found.')
            return
        # All coordinates.
        coords_list = '\n'.join(f"{coord[1]}: X={coord[2]}, Y={coord[3]}, Z={coord[4]}" for coord in all_coords)
        await ctx.send(f'List of coordinates:\n{coords_list}')
        return
    # There is a query.
    cursor.execute('SELECT * FROM coordinates WHERE description LIKE ?', ('%' + query + '%',))
    filtered_coords = cursor.fetchall()
    # Nothing found from the query.
    if not filtered_coords:
        await ctx.send(f'No coordinates found matching the description: {query}')
        return
    # Return the query.
    coords_list = '\n'.join(f"{coord[1]}: X={coord[2]}, Y={coord[3]}, Z={coord[4]}" for coord in filtered_coords)
    await ctx.send(f'List of coordinates matching the description "{query}":\n{coords_list}')
    return

@bot.hybrid_command(name='removecoords')
async def remove(ctx, *, query):
    """
    Command to remove coordinates.

    Parameters:
    - ctx (Context): The context of the command.
    - query (str): Query to identify coordinates for removal.

    This function removes coordinates based on the provided exact query.
    """
    # Remove coordinates from the database with an exact match
    cursor.execute('DELETE FROM coordinates WHERE description = ?', (query,))
    conn.commit()

    await ctx.send(f'Coordinates with the exact description "{query}" have been removed.')
    return

if __name__ == '__main__':
    try:
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')
        bot.run(TOKEN)
    finally:
        conn.close()