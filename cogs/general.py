import discord
import random
from discord.ext import commands
from discord.commands import slash_command
from config import both_servers


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=both_servers)
    async def pfp(self, ctx, user: discord.User = None):
        """GOON BOT BEATS BONGO 1000:1"""
        if user is None:
            selected_user = ctx.author
        else:
            selected_user = user

        pfp_url = selected_user.display_avatar.url

        embed = discord.Embed(color=discord.Color.blurple())
        embed.set_author(name=f"{selected_user.name} 📸", url=pfp_url)
        embed.set_image(url=pfp_url)
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=both_servers)
    async def vtuber(self, ctx):
        """Better than ever!"""
        await ctx.send("🤫", delete_after=1)

    @slash_command(guild_ids=both_servers)
    async def coinflip(self, ctx):
        """Gives you heads or tails"""
        coin = random.choice(["Heads", "Tails"])
        await ctx.respond(embed=discord.Embed(title=coin, color=discord.Color.blurple()))

    @slash_command(guild_ids=both_servers)
    async def wni(self, ctx):
        """Wow, no invite?"""
        complaint = random.choice(
            [
                "Wow, no invite?",
                "WOW..no invite?",
                "My invite must have gotten lost in the mail",
                "Wow no invite?",
                "WOW. NOT INVITED, NOT SURPRISED.",
                "WOW. NO INVITE, NOT SURPRISED.",
                "come on man not cool",
                "i thought we were friends",
                "guess ill hangout here... alone... again",
                "hey, come on! I like darts too",
            ]
        )
        await ctx.respond(embed=discord.Embed(title=complaint, color=discord.Color.blurple()))


def setup(bot):
    bot.add_cog(General(bot))
