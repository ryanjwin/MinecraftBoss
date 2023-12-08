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

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

    if bot.guilds:
        # Find the first text channel the bot has access to in the guild
        if bot.guilds[0].text_channels:
            text_channel = bot.guilds[0].text_channels[0]
            await text_channel.send('Hello everyone!')


if __name__ == '__main__':
    try:
        load_dotenv()
        TOKEN = os.getenv('DISCORD_TOKEN')
        bot.run(TOKEN)
    finally:
        conn.close()