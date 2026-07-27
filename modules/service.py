import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

class ServiceMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_usr = os.getenv('admin_usr')

        self.service_err = "Something went wrong.\nHave you added the service entries to the .env file?"
        self.not_allowed = "You're not allowed to use this command."


    @commands.hybrid_command(
            name='service',
            help="List active/inactive systemd services.\nUses systemctl (systemd)\n\nlist            -> List entries in the '.env' file\nstatus          -> List service entries and check if they're active\nstatus-detailed -> Same as above, but with details (systemctl status [service name])\nupdate-env      -> Create 'service_list' variable in the .env file\nabout           -> More information about the module\n[service name]  -> Show current status of service in systemd")
    @app_commands.describe(mode="list, status, status-detailed, update-env, about, [service name]")
    async def service_cmd(self, ctx, mode = commands.parameter(description="- list, status, status-detailed, update-env, about, [service name]")):
        if str(ctx.message.author.id) not in self.admin_usr:
            await ctx.send(self.not_allowed)
            return

        if mode == 'list':
            listdir_env = os.getenv('service_list')
            if listdir_env is None:
                await ctx.reply(self.service_err)
                return
            await ctx.send(f'**Service Entries:**\n{listdir_env}')

        elif mode == 'status':
            try:
                listdir_env = os.getenv('service_list')
                listdir = [item.strip() for item in listdir_env.split(',')]
                message = "**Service Activity:**\n"
                for file in listdir:
                    message += f"```{file}: {subprocess.getoutput([f'systemctl is-active {file}'])}```"
                await ctx.send(message)
            except:
                await ctx.reply(self.service_err)

        elif mode == 'status-detailed':
            try:
                listdir_env = os.getenv('service_list')
                listdir = [item.strip() for item in listdir_env.split(',')]
                await ctx.send("**Service Activity:**")
                for file in listdir:
                    await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl status {file}'])}```")
            except:
                await ctx.reply(self.service_err)

        elif mode == 'update-env':
            try:
                await ctx.send("Adding 'service_list' to the .env file...")
                env = open(f'.env', 'a', encoding='utf-8')
                env.write("\n#Service_module\nservice_list = ','\n")
                env.close()
                await ctx.send("Updated successfully the .env file. It's recommended to restart the bot.")
            except Exception as err:
                await ctx.reply(f"Failed to update the .env file: {err}")

        elif mode == 'about':
            await ctx.send(
"""
**Service Monitor**
```List active/inactive systemd services. To add service entry, enter service name in the .env file (service_list)
Uses systemctl (systemd)

list            -> List entries in the .env file
status          -> List service entries and check if they're active
status-detailed -> Same as above, but with details (systemctl status [service name])
update-env      -> Create 'service_list' variable in the .env file
about           -> See this message
[service name]  -> Show current status of selected service in systemd```
""")

        else:
            try:
                await ctx.send(f"**Service {mode}:**\n```{subprocess.getoutput([f'systemctl status {mode}'])}```")
            except Exception as err:
                await ctx.send(f'Something went wrong.\nPossible cause: {err}')


    @service_cmd.error
    async def service_cmd_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing argument.\nUsage: .service { list | status | status-detailed | update-env | about | [service name] }")
        else:
            await ctx.reply(f'Something went wrong.\nPossible cause: {error}')


async def setup(bot):
    await bot.add_cog(ServiceMonitor(bot)) 