import random
from os import name

import discord
from config import all_servers
from discord.commands import slash_command
from discord.ext import commands


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def make_art_embed(ctx: discord.ApplicationContext, image) -> None:

        art_embed = discord.Embed()

        if isinstance(image, str):
            art_embed.set_image(url=image)
        elif isinstance(image, list):
            image = random.choice(image)
            art_embed.set_image(url=image)

        art_embed.set_author(name=ctx.command.name)  # type: ignore
        art_embed.color = discord.Color.blurple()
        await ctx.respond(embed=art_embed)  # type: ignore

    @slash_command()
    async def bringe(self, ctx: discord.ApplicationContext):
        """Better Cringe. Duh."""
        image = "https://cdn.discordapp.com/attachments/531913512822243358/651997904751427624/Hudboy.png"
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def gamerword(self, ctx: discord.ApplicationContext):
        """Small child with heart of stone"""
        image = "https://cdn.discordapp.com/attachments/531913512822243358/651997280290734101/gamer.jpg"
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def pizza(self, ctx: discord.ApplicationContext):
        """finna get pizza pied"""
        image = "https://cdn.discordapp.com/attachments/177125557954281472/731242309446008893/image0.jpg"
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def clown(self, ctx: discord.ApplicationContext):
        """...he's the joker...baby..."""
        image = "https://cdn.discordapp.com/attachments/177125557954281472/651996397041877006/clown_2.0.jpg"
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def ygg(self, ctx: discord.ApplicationContext):
        """You good girl?"""
        image = "https://cdn.discordapp.com/attachments/" "733685825379893339/756322976034586654/c00a411b-1fea-4593-b528-56cfc2dea9cf.png"
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def frog(self, ctx: discord.ApplicationContext):
        """Fantasy Frog Fetish"""
        image = [
            "https://i.imgur.com/lqZM3sR.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/814729226031726632/1614310329958.jpg",
            "https://media1.tenor.com/images/ba97a5584efb72bdfa4feeacc83ea2c2/tenor.gif",
            "https://media1.tenor.com/images/bfeaafa2ff74d740f1920174ce796ef3/tenor.gif",
        ]
        await self.make_art_embed(ctx, image)

    @slash_command()
    async def joker(self, ctx):
        """Lex Fully Evolved"""
        image = "https://cdn.discordapp.com/attachments/" "177125557954281472/754429776571138238/lex_true_form.jpg"
        await self.make_art_embed(ctx, image)

    @slash_command(name="real")
    async def real(self, ctx: discord.ApplicationContext):
        """Evidence of paranormal cativity and other anomalies"""
        # Alt doc string: Anything made to be remotely realistic OR paranormal can be added here
        # It's a dumpster fire at this point 🔥
        #                                    🗑
        evidence = [
            "https://cdn.discordapp.com/attachments/177125557954281472/810598965190983720/1612730989587.gif",
            "https://media1.tenor.com/images/5416c3b664a81ad99275761d701edcfd/tenor.gif?itemid=16255347",
            "https://cdn.discordapp.com/attachments/177125557954281472/938132511270240356/1643438475633.gif",
            "https://cdn.discordapp.com/attachments/177125557954281472/937579976159526942/1643578958193.gif",
            "https://cdn.discordapp.com/attachments/177125557954281472/937577902113972254/1643260137906.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/936873848001929276/1643437992106.png",
            "https://tenor.com/view/cat-naenae-gif-21093090.gif",
            "https://tenor.com/view/cat-dance-dancing-cat-gif-13017095.gif",
            "https://tenor.com/view/cat-dance-dancing-happy-moves-gif-4685977.gif",
            "https://tenor.com/view/alien-baby-gif-6385576.gif",
            "https://tenor.com/view/ruler-gif-23178618.gif",
            "https://tenor.com/view/grey-roswell-scary-autopsy-alien-gif-12272832.gif",
            "https://tenor.com/view/extraterrestrial-grey-ufo-abduction-scary-gif-12272827.gif",
            "https://cdn.discordapp.com/attachments/177125557954281472/902737733812895824/MATT.png",
            "https://tenor.com/view/cat-dance-dancing-stand-gif-3536175.gif",
        ]
        await self.make_art_embed(ctx, evidence)

    @slash_command()
    async def rool(self, ctx: discord.ApplicationContext):
        """G8r man!"""
        image = "https://media1.tenor.com/images/c071dcb215cc774f730c1630a5971fb4/tenor.gif?itemid=12340096"
        await self.make_art_embed(ctx, image)


def setup(bot):
    bot.add_cog(Art(bot))
