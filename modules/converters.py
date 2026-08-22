import discord
from discord.ext import commands
from discord import app_commands


ver = 2.0
dec_num_text = "Decimal number"


class Converters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

            #Converters
    #1
    @commands.hybrid_command(
        name='convert', 
        help=f"Advanced Converter v{ver}\n========================\n\nConverts one number to other number systems - binary, octal, decimal, hexa (hexadecimal)"
    )
    @app_commands.describe(
        type   = "{ binary | octal | decimal | hexa | about }",
        number = "The number to convert"
    )
    async def multiconv(
        self, ctx, 
        type   = commands.parameter(description="{ binary | octal | decimal | hexa | about }"),
        number = commands.parameter(description="The number to convert", default=None)
    ):

        try:
            if type == 'decimal':
                number = int(number)
                hexa = hex(number)
                octa = oct(number)
                bina = bin(number)
                try:
                    await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa}\nDecimal: {number}\nOctal: {octa}\nBinary: {bina}')
                except:
                    await ctx.send(f'Unexpected Error\nPlease try again')

            elif type == 'octal':
                deci = int(number, base=8)
                bina1 = int(number, base=8)
                bina2 = bin(bina1)
                hexa1 = int(number, base=8)
                hexa2 = hex(hexa1)
                try:
                    await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa2}\nDecimal: {deci}\nOctal: {number}\nBinary: {bina2}')
                except:
                    await ctx.send(f'Unexpected Error\nPlease try again')

            elif type == 'binary':
                deci = int(number, base=2)
                octa1 = int(number, base=2)
                octa2 = oct(octa1)
                hexa1 = int(number, base=2)
                hexa2 = hex(hexa1)
                try:
                    await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa2}\nDecimal: {deci}\nOctal: {octa2}\nBinary: {number}')
                except:
                    await ctx.send(f'Unexpected Error\nPlease try again')

            elif type == 'hexa':
                deci = int(number, base=16)
                octa1 = int(number, base=16)
                octa2 = oct(octa1)
                bina1 = int(number, base=16)
                bina2 = bin(bina1)
                try:
                    await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {number}\nDecimal: {deci}\nOctal: {octa2}\nBinary: {bina2}')
                except:
                    await ctx.send(f'Unexpected Error\nPlease try again')
            elif type == 'about':
                await ctx.send(
f"""
Advanced Converter v{ver}
========================

Converts one number to other number systems - binary, octal, decimal, hexa (hexadecimal).
Example: .convert hexa 7D7 -> converts hexadecimal '7D7' to other number systems
Source: [Converter on GitHub](https://github.com/kamile320/ConverterDiscordModule)

Changelog:
- Moved commands to separate cog/module.
- Updated commands to hybrid commands.
- Small improvements. Added 'about' option to '.convert' command.
"""
)

            else:
                await ctx.send('Wrong value.\nType: .convert binary/octal/decimal/hexa and value for selected number system')
        except Exception as err:
            await ctx.send(f'Unexpected error occurred: {err}')


    #2
    @commands.hybrid_command(
        name='binary', 
        help="Convert decimal number to binary.\n.binary <dec number>"
    )
    @app_commands.describe(
        number=dec_num_text
    )
    async def binary(
        self, ctx, 
        number = commands.parameter(description=dec_num_text)
    ):

        binn = bin(int(number))
        await ctx.send(f'{number} in binary: {binn}')


    #3
    @commands.hybrid_command(
        name='hexa', 
        help="Convert decimal number to hexadecimal.\n.hexa <dec number>"
    )
    @app_commands.describe(
        number=dec_num_text
    )
    async def hexadecimal(
        self, ctx, 
        number = commands.parameter(description=dec_num_text)
    ):

        hexa = hex(int(number))
        await ctx.send(f'{number} in hexadecimal: {hexa}')
            #Converters-END

async def setup(bot):
    await bot.add_cog(Converters(bot)) 