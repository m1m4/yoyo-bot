# bot.py

import os
import discord
import random
import json
import traceback
import get_jokes

from dotenv import load_dotenv
from discord.ext import commands

# Load enviroment variables
load_dotenv()

# The token
TOKEN = os.getenv('DISCORD_TOKEN')
# The name of my server
# Directory path of the server application
PATH = os.path.dirname(os.path.realpath(__file__))

# Set the intents so the bot will work
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} connected to discord')
    get_jokes.main()


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name} Initiating moist infrastructure... !'
    )


@bot.command(name='roll_dice', aliases=['r', 'roll'], help='Simulates rolling dice.')
async def roll(ctx, dice_count: int = 1):
    if dice_count <= 0:
        await ctx.send("יפסיכופת מה שלילי")
        return

    if dice_count > 100:
        await ctx.send(random.choice("תרגע אחי", "לא הגזמת בכלל"))
        return

    dice = [random.choice(range(1, 7))
            for _ in range(dice_count)]

    await ctx.send('__Result:__ \n')

    # Send multiple messages if dice_count > 15
    for _ in range(int(len(dice) / 10 + 1)):
        await ctx.send(create_dice_message(dice[:10]))

        for d in range(15):
            dice.pop(0)


# Creates the dice message
def create_dice_message(dice):
    side_1 = (':white_large_square::white_large_square::white_large_square:',
              ':white_large_square::white_square_button::white_large_square:',
              ':white_large_square::white_large_square::white_large_square:')

    side_2 = (':white_square_button::white_large_square::white_large_square:',
              ':white_large_square::white_large_square::white_large_square:',
              ':white_large_square::white_large_square::white_square_button:')

    side_3 = (':white_square_button::white_large_square::white_large_square:',
              ':white_large_square::white_square_button::white_large_square:',
              ':white_large_square::white_large_square::white_square_button:')

    side_4 = (':white_square_button::white_large_square::white_square_button:',
              ':white_large_square::white_large_square::white_large_square:',
              ':white_square_button::white_large_square::white_square_button:')

    side_5 = (':white_square_button::white_large_square::white_square_button:',
              ':white_large_square::white_square_button::white_large_square:',
              ':white_square_button::white_large_square::white_square_button:')

    side_6 = (':white_square_button::white_large_square::white_square_button:',
              ':white_square_button::white_large_square::white_square_button:',
              ':white_square_button::white_large_square::white_square_button:')

    sides = {1: side_1, 2: side_2, 3: side_3, 4: side_4, 5: side_5, 6: side_6}

    final = ''

    for i in range(3):
        for d in dice:
            side = sides.get(d)
            final += side[i] + '   '

        final += '\n'

    return final


@bot.command(name='prefix', aliases=['p'], help='Repeats your message.')
async def repeat(ctx, *msg):
    if msg:
        await ctx.send(' '.join(msg))
    else:
        await ctx.send("מעוך רצח")


@bot.command(name='create-channel')
@commands.has_role('fr')
async def create_channel(ctx, channel_name='giant-t-rex'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='repeat', help='Repeats your message.')
async def repeat(ctx, *msg):
    if msg:
        await ctx.send(' '.join(msg))
    else:
        await ctx.send("מעוך רצח")


@bot.command(name='yoyo', aliases=['y'], help='Gives you an awesome joke.')
async def send_joke(ctx, cat: str = None):

    try:
        jokes_dict = json.loads(open(PATH + r'\jokes\dict.json', 'r').read())
        jokes_list = list(jokes_dict)

        if not cat:
            cat = random.choice(jokes_list)

        file = open(PATH + r'\jokes\jokes-' + cat + '.txt', 'rb')
        rand_line = random.randrange(1, len(file.readlines()))
        file.close()

        file = open(PATH + r'\jokes\jokes-' + cat + '.txt', 'rb')
        joke = file.readlines()[rand_line].decode()
        file.close()

    except:
        traceback.print_exc()
        return

    await ctx.send(joke)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('אחי זה אפילו לא כתוב טוב')
        await ctx.send(error)


bot.run(TOKEN)
