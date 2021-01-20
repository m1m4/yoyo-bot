# essentials.py

import traceback
from discord.ext import commands


# Essential and basic functions for the bot

class Essentials(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='repeat', help='Repeats your message.')
    async def repeat(self, ctx, *msg):
        if msg:
            await ctx.send(' '.join(msg))
        else:
            await ctx.send("מעוך רצח")

    @commands.command(name='aliases', aliases=['a'], help='Sends all the aliases of the given command.')
    async def aliases(self, ctx, message: str):
        try:
            command = commands.Bot.get_command(self.bot, message)

            if not command:
                raise commands.BadArgument

            command_aliases = command.aliases
            command_name = command.name

            final = f'`.{command_name}` has {str(len(command_aliases))} aliases: '
            for alias in command_aliases:
                final += f'`.{alias}` '

            await ctx.send(final)

        except commands.BadArgument:
            raise commands.BadArgument

        except:
            traceback.print_exc()

    @commands.command(name='prefix', aliases=['p'], help='Repeats your message.')
    async def set_prefix(self, ctx, *msg):
        if msg:
            await ctx.send(' '.join(msg))
        else:
            raise commands.BadArgument
