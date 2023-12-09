# Minecraft Boss Discord Bot

## Introduction

The Minecraft Boss Bot is a Discord bot designed to enhance the management of a Minecraft server. It facilitates the storage and retrieval of coordinates and is planned to include additional features such as project lists, item lists for projects, and recipe books for crafting.

## Features

- **Coordinate Storage:** Save and retrieve coordinates for locations in the Minecraft world.

## Commands

- **/hello:** Greet the bot.

- **/h:** Display information about available commands.

- **/savecoords:** Save coordinates for locations in the Minecraft world.

   Example: `/savecoords description x y z`

- **/coords:** List stored coordinates. Optionally filter by providing a query.

   Example: `/coords query`

- **/removecoords:** Remove coordinates based on an exact query.

   Example: `/removecoords query`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ryanjwin/MinecraftBoss.git
   ```
2. Install the dependencies
   ```pip
   pip install -r requirements.txt
   ```
3. Create your .env file for the bot token you created [here](https://discord.com/developers/applications)
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot on your server or computer.  I recommend using *screen*
   ```bash
   python3 bot.py
   ```

## Future Updates

- **Project Lists:** Manage and display lists of ongoing projects on the server.

- **Item Lists:** Keep track of required items for each project.

- **Recipe Books:** Access crafting recipes for in-game items.

## Contributions

Contributions are welcome! If you have ideas for improvements or additional features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://github.com/ryanjwin/MinecraftBoss/blob/main/LICENSE).
