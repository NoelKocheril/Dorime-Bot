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
import re

# See Sample.env for example of what the .env file should look like
config = dotenv_values(".env")

# Regex Definitions
SPOTIFY_URL_REGEX = re.compile(r"(?i)open\.spotify\.com/track/([a-zA-Z0-9]*)\?.*")

# Update the .env file to swap the DEBUG Value
DEBUG = bool(strtobool(config["DEBUG"])) if "DEBUG" in config else False

# Get Watched Spotify Watched Channel
SPOTIFY_WATCHED_CHANNEL = int(config["WATCHED_SPOTIFY_CHANNEL"])

# Double check that the program is extracting the .env configurations correctly
if DEBUG:
    for key in config:
        print(f"{key}: {config[key]}")

# Random Helper Functions
def get_quote() -> str:
    res = requests.get("https://zenquotes.io/api/random").json()[0]
    return f"\"{res['q']}\" - {res['a']}"


# Dorime Bot Definitions
class DorimeBot(discord.Client):
    async def on_ready(self) -> None:
        """Will display which user we are connecting to when the discord bot connects to the server"""

        print(f"We Have Logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        """
        Describes how to handle messages that the bot sees

        :param discord.Message message: The incoming message
        :return None
        """

        # If the message is coming from the ignore...
        if message.author == self.user:
            return

        author: discord.User = message.author
        channel: discord.TextChannel = message.channel

        if DEBUG:
            print(
                f"channel.id ({channel.id}) == SPOTIFY_WATCHED_CHANNEL ({SPOTIFY_WATCHED_CHANNEL}): {channel.id == SPOTIFY_WATCHED_CHANNEL}"
            )

        # If the message starts with $hello, reply with Hello
        if channel.id == SPOTIFY_WATCHED_CHANNEL:
            if DEBUG:
                print("Message sent in Spotify Watch Channel")

            spotify_track_ids = re.findall(SPOTIFY_URL_REGEX, message.content)

            if DEBUG and not spotify_track_ids:
                print("No Spotify Track URL found in Message")
                return

            await message.channel.send(
                f"Found the Spotify URL with the Track id(s): {spotify_track_ids}"
            )

            # TODO: Add Track id to Spotify Playlist

        elif message.content.startswith("$hello"):
            msg = f"Hello <@{author.id}>!"
            await message.channel.send(msg)
        elif message.content.startswith("$inspire"):
            quote = get_quote()
            await message.channel.send(quote)
        elif message.content.startswith("$here"):

            print(message)


def main():
    # Start the bot with Bot Token from the .env file
    client = DorimeBot()
    client.run(config["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
