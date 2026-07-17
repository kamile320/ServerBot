import discord
from discord.ext import commands
from discord import app_commands

#It's a simple template for creating a cog

class TemplateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test', description="Test command")
    async def test(self, ctx):
        await ctx.send("Test message")

    @app_commands.command(name='test', description="Test command")
    async def test_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test message")

async def setup(bot):
    await bot.add_cog(TemplateCog(bot)) 