import discord
import spotipy
from distutils.util import strtobool
from dotenv import dotenv_values

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


def main():
    # Start the bot with Bot Token from the .env file
    client.run(config["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
