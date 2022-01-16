""" This runs the bot """
import discord
import os
from dotenv import load_dotenv
from config import console, __version__
from modules.init_functions import collect_cogs, load_cogs

bot = discord.Bot()


@bot.event
async def on_ready():
    """Event that runs when bot has successfully connected"""
    console.log(f"{bot.user} has started")
    await bot.change_presence(activity=discord.Game(name=__version__))


""" TODO This worked in dpy, unsure what the new implementation is"""
# @bot.event
# async def on_command(ctx):
#     """Log ever command used"""
#     message = ctx.message
#     content = message.content
#     goon = message.author.name
#     console.log(f"{goon} used {content}")


if __name__ == "__main__":
    console.rule(f"Goonbot 4 ({__version__})")
    collect_cogs()
    load_cogs(bot)
    load_dotenv()
    bot.run(os.getenv("DISCORD"))
