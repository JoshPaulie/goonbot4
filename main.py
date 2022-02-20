""" This runs the bot """
import os

import discord
import dotenv

from config import __version__, all_servers, console
from modules.init_functions import collect_cogs, load_cogs

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)
bot.debug_guilds = all_servers


@bot.event
async def on_ready():
    """Event that runs when bot has successfully connected"""
    console.log(f"{bot.user.name} has started")  # type: ignore
    await bot.change_presence(activity=discord.Game(name=__version__))


@bot.event
async def on_application_command(ctx: discord.ApplicationContext):
    console.log(f"{ctx.author.name} used [underline]{ctx.command.qualified_name}[/]")


if __name__ == "__main__":
    console.rule(f"🤖 Goonbot 4 ({__version__})")
    collect_cogs()
    load_cogs(bot)
    dotenv.load_dotenv()
    bot.run(os.getenv("DISCORD"))
