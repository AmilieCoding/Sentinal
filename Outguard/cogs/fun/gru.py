import discord
from discord.ext import commands
import random

# -> THIS IS AN INSIDE JOKE. DON'T WORRY LMAO.
class GruCog(commands.Cog):
    gru_gifs = [
        "https://media.tenor.com/mEhkr91yX5YAAAAM/gru-moon.gif",
        "https://media2.giphy.com/media/13Iu9mjLpXF0ek/200w.gif?cid=6c09b952k6v3tku6b286zer8l3sf9z90719jqvk4qwetecoh&ep=v1_gifs_search&rid=200w.gif&ct=g",
        "https://media2.giphy.com/media/62TTKM9F5B5ni/200w.gif?cid=6c09b952uzjpjywettopi47ay9s8gnabf1gdicg6wz09wecq&ep=v1_gifs_search&rid=200w.gif&ct=g",
        "https://64.media.tumblr.com/a44ee02d89f4ab537c12b12024bcf4ae/tumblr_moeczodsZ11s8njeuo1_400.gif",
        "https://media0.giphy.com/media/fYl6op4uTBUBy/giphy.gif?cid=6c09b952k6v3tku6b286zer8l3sf9z90719jqvk4qwetecoh&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        "https://media3.giphy.com/media/E64BKbLdCaqRi/giphy.gif?cid=6c09b952uzjpjywettopi47ay9s8gnabf1gdicg6wz09wecq&ep=v1_gifs_search&rid=giphy.gif&ct=g"
    ]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="gru", description="Random Gru GIF iykyk")
    async def gru(self, ctx: commands.Context):
        selected_gif = random.choice(self.gru_gifs)  # Access class attribute
        embed = discord.Embed(color=discord.Color.from_rgb(255, 255, 255))
        embed.set_image(url=selected_gif)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(GruCog(bot))
