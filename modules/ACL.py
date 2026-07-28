import discord
from discord.ext import commands
import os
import datetime
import shutil
import dotenv



#Messages-Informations-Errors
ACL_user_not_found         = "User history not found."
ACL_history_not_found      = "Global message history does not exist."
ACL_nopermission           = "You don't have permission to use ACL mode. This incident will be reported."
ACL_rm_all_success         = "Cleared all saved message history."
ACL_rm_all_fail            = "Cannot clear all message history."
ACL_rm_user_fail           = "Cannot clear message history of the selected user. Does it even exist?"
ACL_dotenv_fail            = "[ACL] CAN'T LOAD .env FILE!\nCreate .env file with the variables below and reload the module:\nadmin_usr = ['your Discord ID']\nextendedErrMess = True/False\nglobalLog = True/False\nuntrackableUser = ['user/channel/server ID']\nThe .env file should be located in the bot main directory."
ACL_server_create_fail     = "[ACL] Cannot create server entry."
ACL_channel_create_fail    = "[ACL] Cannot create channel entry."
ACL_user_create_fail       = "[ACL] Cannot create user entry."
ACL_global_create_fail     = "[ACL] Cannot create global message history entry."
ACL_message_write_fail     = "[ACL] Failed to save a message."
ACL_channel_not_found      = "Channel history not found."
ACL_create_fail            = "Cannot create ACL directory."
ACL_server_not_found       = "Server history not found."
ACL_rm_server_success      = "Removed server history."
ACL_rm_server_fail         = "Failed to remove server history."
ACL_rm_channel_success     = "Removed channel history."
ACL_rm_channel_fail        = "Failed to remove channel history."
ACL_rm_global_success      = "Removed global message history."
ACL_rm_global_fail         = "Failed to remove global message history."
ACL_global_log_disabled    = "Global log is disabled. Enable it in the .env file."
ACL_no_value_ID            = "Incomplete command. Type correct ID."
ACL_wrong_mode             = "Wrong mode selected. See '.help ACL' for more info."
ACL_incomplete_command     = "Incomplete command. See '.help ACL' for more info."
ACL_rm_all_pending         = "Removing all collected history..."
ACL_rm_user_pending        = "Removing user history..."
ACL_rm_server_pending      = "Removing server history..."
ACL_rm_channel_pending     = "Removing channel history..."
ACL_rm_global_pending      = "Removing global message history..."
cmd_help_val               = "Manage A.C.L. user message history\nget { user | server | channel } <ID> - Show message history by selected type and ID.\nget history - (global) history of all saved messages.\nclear { all | user | server | channel | global } [ID] - Removes selected type of saved messages; ID required when { user | server | channel } selected.\nupdate-env - Add required variables to the '.env' file.\n\nUse '.ACL about' for more information."
cmd_mode_desc              = "Selected mode { get | clear | update-env | about }."
cmd_value_desc             = "Type of subject { user | server | channel | history | all | global }."
cmd_value2_desc            = "Subject - ID of user/server/channel if required by selected operation."
ACL_env_create_pending     = "Adding ACL variables to the .env file..."
ACL_env_create_success     = "Updated successfully the .env file. Enter correct values or remove duplicated variables and restart your discord bot."
ACL_env_create_fail        = "Failed to update the .env file:"



class AdvancedChannelListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ACLver = "5.0"
        self.displayname='A.C.L.'
        self.maindir = os.path.dirname(os.path.abspath(__file__))
        self.accept_value = ['true', 'enabled', 'ena', 'yes', 'y', '1', 1, True]

        try:
            dotenv.load_dotenv()
            ################# Tokens/IDs/etc ###################
            self.admin_usr        = os.getenv('admin_usr') or ''
            self.extendedErrMess  = str(os.getenv('extendedErrMess')).lower() or ''
            self.global_Log       = str(os.getenv('globalLog')).lower() or ''
            self.untrackableUsr   = os.getenv('untrackableUser') or ''
            ####################################################
        except Exception as err:
            if self.extendedErrMess in self.accept_value:
                print(f"{ACL_dotenv_fail}\nException: {err}")
            else:
                print(ACL_dotenv_fail)

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
            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_create_fail} Exception: {err}')
                else:
                    print(ACL_create_fail)


    #Time
    def time(self):
        return datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')


    #MessageLogging
    def userLog(self, usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
        if str(srv_id) in self.untrackableUsr or str(chnl_id) in self.untrackableUsr or str(usr_id) in self.untrackableUsr:
            return
        time = self.time()
        if os.path.exists(f'{self.maindir}/ACL/User/{usr_id}/message.txt') == True:
            try:
                with open(f'{self.maindir}/ACL/User/{usr_id}/message.txt', 'a', encoding='utf-8') as usrmessage:         
                    usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
           
            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_message_write_fail}\nException: {err}')
                else:
                    print(ACL_message_write_fail)

        else:
            print("[ACL] New user detected. Creating new entry...")
            try:
                os.makedirs(f'{self.maindir}/ACL/User/{usr_id}')
                with open(f'{self.maindir}/ACL/User/{usr_id}/message.txt', 'a', encoding='utf-8') as usrmessage
                    usrmessage.write(f'{self.displayname} user message log\nUsername: {usr}\nUserID: {usr_id}\nDetected: {time}\n##############################\n\n')
                    usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
        
            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_user_create_fail}\nException: {err}')
                else:
                    print(ACL_user_create_fail)



    def globalLog(self, usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
        if str(srv_id) in self.untrackableUsr or str(chnl_id) in self.untrackableUsr or str(usr_id) in self.untrackableUsr:
            return
        time = self.time()
        if os.path.exists(f'{self.maindir}/ACL/global.txt') == True:
            try:
                with open(f'{self.maindir}/ACL/global.txt', 'a', encoding='utf-8') as usrmessage:
                    usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
                
            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_message_write_fail}\nException: {err}')
                else:
                    print(ACL_message_write_fail)

        else:
            print("[ACL] Global message history not detected. Creating new entry...")
            try:
                with open(f'{self.maindir}/ACL/global.txt', 'a', encoding='utf-8') as usrmessage
                    usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
                
            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_global_create_fail}\nException: {err}')
                else:
                    print(ACL_global_create_fail)



    def serverLog(self, usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
        if str(srv_id) in self.untrackableUsr or str(chnl_id) in self.untrackableUsr or str(usr_id) in self.untrackableUsr:
            return
        time = self.time()
        message = f'[{time}] [{srv} / {chnl}] {usr}({usr_id}): {usrmsg}\n'
        print(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}")
        if os.path.exists(f'{self.maindir}/ACL/Server/{srv_id}') == True:
            try:
                with open(f'{self.maindir}/ACL/Server/{srv_id}/serverlog.txt', 'a', encoding='utf-8') as usrmessage:
                    usrmessage.write(message)
                

            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_message_write_fail}\nException: {err}')
                else:
                    print(ACL_message_write_fail)

        else:
            print("[ACL] New server detected. Creating new entry...")
            try: 
                os.makedirs(f'{self.maindir}/ACL/Server/{srv_id}')

                with open(f'{self.maindir}/ACL/Server/{srv_id}/serverlog.txt', 'a', encoding='utf-8') as usrmessage:
                    usrmessage.write(f'{self.displayname} server message log\nGuild name: {srv}\nGuildID: {srv_id}\nDetected: {time}\n##############################\n\n')
                    usrmessage.write(message)
                

            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_server_create_fail}\nException: {err}')
                else:
                    print(ACL_server_create_fail)

        if os.path.exists(f'{self.maindir}/ACL/Server/{srv_id}/{chnl_id}.txt') == True:
            try:
                usrmessage = open(f'{self.maindir}/ACL/Server/{srv_id}/{chnl_id}.txt', 'a', encoding='utf-8')
                usrmessage.write(message)
                usrmessage.close()

            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_message_write_fail}\nException: {err}')
                else:
                    print(ACL_message_write_fail)

        else:
            print("[ACL] New channel detected. Creating new entry...")
            try: 
                with open(f'{self.maindir}/ACL/Server/{srv_id}/{chnl_id}.txt', 'a', encoding='utf-8') as usrmessage:
                    usrmessage.write(f'{self.displayname} channel message log\nChannel name: {chnl}\nChannelID: {chnl_id}\nIn Guild: {srv}({srv_id})\nDetected: {time}\n##############################\n\n')
                    usrmessage.write(message)

            except Exception as err:
                if self.extendedErrMess in self.accept_value:
                    print(f'{ACL_channel_create_fail}\nException: {err}')
                else:
                    print(ACL_channel_create_fail)


    #LogMessage
    def logMessage(self, info):
        time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        with (f'{self.maindir}/Logs.txt', 'a', encoding='utf-8') as logs:
            logs.write(f'[{time}] {info}\n')
        
    #PrintMessage
    def printMessage(self, info):
        time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f'[{time}] {info}')


    async def on_message_hook(self,message):
        #Username
        username = str(message.author)

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


        if self.global_Log in self.accept_value:
            self.globalLog(username, user_message, channel, server, userid, channelid, serverid)
        self.serverLog(username, user_message, channel, server, userid, channelid, serverid)
        self.userLog(username, user_message, channel, server, userid, channelid, serverid)


    #1
    @commands.command(name='ACL', help=cmd_help_val)
    async def ACL(self, ctx, 
        mode    = commands.parameter(default=None, description=cmd_mode_desc), 
        value   = commands.parameter(default=None, description=cmd_value_desc), 
        value2  = commands.parameter(default=None, description=cmd_value2_desc)
    ):
        if str(ctx.message.author.id) not in self.admin_usr:
            await ctx.send(self.ACL_nopermission)
            message = f"Information[ACL]: User {ctx.message.author.id} tried to use .ACL command without permission.\nSee {self.maindir}/ACL/Users/{ctx.message.author.id} for more information.\n"
            self.printMessage(message)
            self.logMessage(message)
            return

        if mode is None:
            await ctx.send(ACL_incomplete_command)
            return

        #ACL get
        if mode == 'get':
            if value == 'user':#    Get complete user message history of selected user
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/User/{value2}/message.txt'))
                except Exception as err:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_user_not_found}\n{err}")
                    else:
                        await ctx.send(ACL_user_not_found)
                return


            elif value == 'server':#    Get complete user message history from selected server
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/Server/{value2}/serverlog.txt'))
                except Exception as err:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_server_not_found}\n{err}")
                    else:
                        await ctx.send(ACL_server_not_found)
                return


            elif value == 'channel':#   Get complete user message history from selected channel
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                try:
                    server_id = ctx.bot.get_channel(int(value2)).guild.id
                except AttributeError:
                    server_id = "DM"

                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/Server/{server_id}/{value2}.txt'))
                except Exception as err:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_channel_not_found}\n{err}")
                    else:
                        await ctx.send(ACL_channel_not_found)
                return


            elif value == 'history':#   Get complete user message history
                if self.global_Log not in self.accept_value:
                    await ctx.send(ACL_global_log_disabled)
                    return

                try:
                    await ctx.send(file=discord.File(f'{self.maindir}/ACL/global.txt'))
                except:
                    await ctx.send(ACL_history_not_found)
                return


            else:
                await ctx.send(ACL_wrong_mode)



        #ACL clear
        elif mode == 'clear':
            if value == 'all':#   Remove all records
                await ctx.send(ACL_rm_all_pending)
                try:
                    shutil.rmtree(f'{self.maindir}/ACL/')
                    await ctx.send(ACL_rm_all_success)
                    message = f"Information[ACL]: {ACL_rm_all_success}\nCommand executed by: {ctx.author.id}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                except Exception as exc:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_rm_all_fail}\nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_all_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear all message history but failed. \nException: {exc}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                return


            elif value == 'user':#   Remove user records (from /ACL/User)
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                await ctx.send(ACL_rm_user_pending)
                try:
                    shutil.rmtree(f'{self.maindir}/ACL/User/{value2}')
                    await ctx.send(f"Cleared message history of <@{value2}>.")
                    message = f"Information[ACL]: User {ctx.message.author.id} cleared message history of {value2}.\n"
                    self.printMessage(message)
                    self.logMessage(message)
                except Exception as exc:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_rm_user_fail} \nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_user_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of {value2} but failed. \nException: {exc}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                return


            elif value == 'server':#   Remove server records (with separate records of channels)
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                await ctx.send(ACL_rm_server_pending)
                try:
                    shutil.rmtree(f'{self.maindir}/ACL/Server/{value2}')
                    await ctx.send(f"Cleared message history of ServerID({value2}).")
                    message = f"Information[ACL]: User {ctx.message.author.id} cleared message history of ServerID({value2}).\n"
                    self.printMessage(message)
                    self.logMessage(message)
                except Exception as exc:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_rm_server_fail} \nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_server_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of ServerID({value2}) but failed. \nException: {exc}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                return


            elif value == 'channel':#   Remove channel records
                if value2 is None:
                    await ctx.send(ACL_no_value_ID)
                    return

                await ctx.send(ACL_rm_channel_pending)

                try:
                    server_id = ctx.bot.get_channel(int(value2)).guild.id
                except AttributeError:
                    server_id = "DM"

                try:
                    os.remove(f'{self.maindir}/ACL/Server/{server_id}/{value2}.txt')
                    await ctx.send(f"Cleared message history of ChannelID({value2}).")
                    message = f"Information[ACL]: User {ctx.message.author.id} cleared message history of ChannelID({value2}).\n"
                    self.printMessage(message)
                    self.logMessage(message)
                except Exception as exc:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_rm_channel_fail} \nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_channel_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of ChannelID({value2}) but failed. \nException: {exc}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                return
                

            elif value == 'global':#   Remove global log
                if self.global_Log not in self.accept_value:
                    await ctx.send(ACL_global_log_disabled)
                    return

                await ctx.send(ACL_rm_global_pending)
                try:
                    os.remove(f'{self.maindir}/ACL/global.txt')
                    await ctx.send(ACL_rm_global_success)
                    message = f"Information[ACL]: {ACL_rm_global_success}\nCommand executed by: {ctx.author.id}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                except Exception as exc:
                    if self.extendedErrMess in self.accept_value:
                        await ctx.send(f"{ACL_rm_global_fail}\nException: {exc}")
                    else:
                        await ctx.send(ACL_rm_global_fail)
                    message = f"Information[ACL]: User {ctx.message.author.id} tried to remove global message history but failed. \nException: {exc}\n"
                    self.printMessage(message)
                    self.logMessage(message)
                return
                

            else:
                await ctx.send(ACL_wrong_mode)
                return



        #ACL update-env
        elif mode == 'update-env':
            try:
                await ctx.send(ACL_env_create_pending)
                with open(f'.env', 'a', encoding='utf-8') as env
                    env.write("\n#AdvancedChannelListener\nadmin_usr = ['']\nextendedErrMess = False\nglobalLog = False\nuntrackableUser = ['']\n")
                
                await ctx.send(ACL_env_create_success)
            except Exception as err:
                await ctx.reply(f"{ACL_env_create_fail} {err}")
            return



        #ACL about
        elif mode == 'about':
            await ctx.send("""
***AdvancedChannelListener***
Manage A.C.L. user message history.
```
.ACL { get | clear | update-env | about } { user | server | channel | history | all | global } [ID]


.ACL get { user | server | channel | history } [ID] - See message history of selected type. ID is required while selecting { user | server | channel }.
Option { history } sends global message history.

.ACL clear { all | user | server | channel | global } [ID] - Remove message history of selected type. ID is required while selecting { user | server | channel }.
Option { all } removes ALL saved records. Option { global } only removes global message history.

.ACL update-env - Adds required variables to the '.env' file. If new values were entered while running the bot, it's recommended to restart your discord bot.

.ACL about - See this message.
```
""")
            return



        else:
            await ctx.send(ACL_wrong_mode)
            return



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
- Added more advanced logging system - now ACL logs users, server and channels separately.
- Added more message variables.
- Added untrackableUser variable in the .env file - type there any type of ID 
  and this user/server/channel will have an immunity from logging.
- Global message log (also known as default message log) is now disabled by default.
  You can turn it on in the .env file (globalLog = True/False)
- Updated .ACL command - now you can get user/server/channel history by entering ID and also remove it.
  Added 'update-env' option to add required variables to the '.env' file, and 'about' to see more information about the module.
- Better error handling.
- Updated maindir variable - now module will save the logs in the same directory as ACL.py
- Other improvements and fixes""")

async def setup(bot):
    await bot.add_cog(AdvancedChannelListener(bot))
