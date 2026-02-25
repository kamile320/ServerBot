import discord
from discord.ext import commands
import os
import datetime
import shutil
import dotenv

class AdvancedChannelListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ACLver = "4.0"
        self.displayname='A.C.L.'
        self.maindir = os.getcwd()

        #Messages
        self.ACL_notfounderr = "User history not found."
        self.ACL_historynotfound = "Default message history does not exist."
        self.ACL_nopermission = "You don't have permission to use ACL mode. This incident will be reported."
        self.ACL_rm_all_success = "Cleared all saved message history."
        self.ACL_rm_all_fail = "Can't clear all message history."
        self.ACL_rm_user_fail = "Can't clear message history of the selected user. Does it even exist?"

        try:
            dotenv.load_dotenv()
            ############# token/intents/etc ################
            self.admin_usr = os.getenv('admin_usr')
            self.extendedErrMess = os.getenv('extendedErrMess')
            ################################################
        except:
            print("CAN'T LOAD .env FILE!\nCreate .env file with the following variables:\nadmin_usr = ['your discordID']\nextendedErrMess = True/False")
        
        self.aclcheck()


    #AdvancedChannelListener
    def aclcheck(self):
        print(f"AdvancedChannelListener v{self.ACLver} loaded.")
        if os.path.exists(f'{self.maindir}/ACL') == True:
            print("ACL check OK")
        else:
            print("ACL not found.\nCreating...")
            try:
                os.makedirs(f'{self.maindir}/ACL')
            except:
                print('Cannot create ACL directory.')

    #MessageLogging
    def userLog(self, usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
        time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        if os.path.exists(f'{self.maindir}/ACL/{usr_id}/message.txt') == True:
            usrmessage = open(f'{self.maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
            usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
            usrmessage.close()
        else:
            print("[ACL] New user detected. Creating new entry...")
            os.makedirs(f'{self.maindir}/ACL/{usr_id}')
            usrmessage = open(f'{self.maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
            usrmessage.write(f'{self.displayname} user message log\nUsername: {usr}\nUserID: {usr_id}\n##############################\n\n')
            usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
            usrmessage.close()

    def channelLog(self, usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
        time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}")
        if os.path.exists(f'{self.maindir}/ACL/default/message.txt') == True:
            usrmessage = open(f'{self.maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
            usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
            usrmessage.close()
        else:
            print("[ACL] Default message history not detected. Creating new entry...")
            os.makedirs(f'{self.maindir}/ACL/default')
            usrmessage = open(f'{self.maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
            usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
            usrmessage.close()


    async def on_message_hook(self,message):
        #Username
        username = str(message.author).split('#')[0]

        #UserMessage
        user_message = str(message.content)
        
        #Channel
        try:
            channel = str(message.channel.name)
        except AttributeError:
            channel = str(message.channel)
        
        #Server
        try:
            server = str(message.guild.name)
        except AttributeError:
            server = str(message.guild)
        
        #UserID
        userid = message.author.id
        
        #ChannelID
        channelid = message.channel.id
        
        #ServerID
        try:
            serverid = message.guild.id
        except AttributeError:
            serverid = "DM"


        self.channelLog(username, user_message, channel, server, userid, channelid, serverid)
        self.userLog(username, user_message, channel, server, userid, channelid, serverid)


    #1
    @commands.command(name='ACL', help='Manage A.C.L. users messages saved history\ngetusr - shows User history by User ID\nget history - history of all saved messages\nclear [all/user_id] - removes all saved messages or only messages of selected user')
    async def ACL(self, ctx, mode, *, value):
        if str(ctx.message.author.id) in self.admin_usr:
            if mode == 'getusr':
                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/{value}/message.txt'))
                except:
                    await ctx.send(self.ACL_notfounderr)
            elif mode == 'get' and value == 'history':
                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/default/message.txt'))
                except:
                    await ctx.send(self.ACL_historynotfound)
            elif mode == 'clear':
                if value == 'all':
                    try:
                        shutil.rmtree(f'{self.maindir}/ACL/')
                        await ctx.send(self.ACL_rm_all_success)
                        message = f"Information[ACL]: {self.ACL_rm_all_success} Command executed by: {ctx.author.id}\n"
                        self.printMessage(message)
                        self.logMessage(message)
                    except Exception as exc:
                        if self.extendedErrMess:
                            await ctx.send(f"{self.ACL_rm_all_fail} \nException: {exc}")
                        else:
                            await ctx.send(self.ACL_rm_all_fail)
                        message = f"Information[ACL]: User {ctx.message.author.id} tried to clear all message history but failed. \nException: \n{exc}\n"
                        self.printMessage(message)
                        self.logMessage(message)
                else:
                    try:
                        shutil.rmtree(f'{self.maindir}/ACL/{value}')
                        await ctx.send(f"Cleared message history of <@{value}>.")
                        message = f"Information[ACL]: User {ctx.message.author.id} cleared message history of {value}.\n"
                        self.printMessage(message)
                        self.logMessage(message)
                    except Exception as exc:
                        if self.extendedErrMess:
                            await ctx.send(f"{self.ACL_rm_user_fail} \nException: {exc}")
                        else:
                            await ctx.send(self.ACL_rm_user_fail)
                        message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of {value} but failed. \nException: \n{exc}\n"
                        self.printMessage(message)
                        self.logMessage(message)
            else:
                await ctx.send("Wrong mode. See '.help ACL' for more info")
        else:
            await ctx.send(self.ACL_nopermission)
            message = f"Information[ACL]: User {ctx.message.author.id} tried to use .ACL command without permission.\nSee {self.maindir}/ACL/{ctx.message.author.id} for more information.\n"
            self.printMessage(message)
            self.logMessage(message)
    
    #2
    @commands.command(name='ACLinfo', help='Show info about loaded module')
    async def ACLinfo(self, ctx):
        await ctx.send(f"""
***AdvancedChannelListener***
Version: {self.ACLver}
Main Directory: {self.maindir}
Source: [ACL on GitHub](https://github.com/kamile320/AdvancedChannelListener)

This module saves every message sent in Discord channels. This can break user privacy; you're using this module at your own risk!

Changelog v{self.ACLver}:
- Reworked to a cog module - now you need a bot that uses cogs to run it (like ServerBot).
- Added .ACLinfo command to show info about the module.""")

async def setup(bot):
    await bot.add_cog(AdvancedChannelListener(bot))