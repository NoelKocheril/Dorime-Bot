# Discord Stuff
import discord

# Spotify Stuff
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# Utility Imports
from distutils.util import strtobool
from dotenv import dotenv_values
import requests
import json

# See Sample.env for example of what the .env file should look like
config = dotenv_values(".env")

# Update the .env file to swap the DEBUG Value
DEBUG = bool(strtobool(config["DEBUG"])) if "DEBUG" in config else False

# Double check that the program is extracting the .env configurations correctly
if DEBUG:
    for key in config:
        print(f"{key}: {config[key]}")

# Setup the Discord Client Object
client = discord.Client()


def get_quote() -> str:
    res = requests.get("https://zenquotes.io/api/random").json()[0]
    return f"\"{res['q']}\" - {res['a']}"


@client.event
async def on_ready() -> None:
    """Will display which user we are connecting to when the discord bot connects to the server"""

    print(f"We Have Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    """
    Describes how to handle messages that the bot sees

    :param discord.Message message: The incoming message
    :return None
    """

    # If the message is coming from the ignore...
    if message.author == client.user:
        return

    # If the message starts with $hello, reply with Hello
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
    elif message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)


def main():
    # Start the bot with Bot Token from the .env file
    client.run(config["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
