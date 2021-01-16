# bot.py

import os
import discord
import random
import json
import traceback
import time

from dotenv import load_dotenv
from discord.ext import commands

# Load enviroment variables
load_dotenv()

# The token
TOKEN = os.getenv('DISCORD_TOKEN')
# The name of my server
GUILD = os.getenv('DISCORD_GUILD')
# Directory path of the server application
PATH = os.path.dirname(os.path.realpath(__file__))

# Set the intents so the bot will work
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

retard_mode = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} connected to discord')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('כתוב מעפן תנסה שוב')


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
async def set_prefix(ctx, *msg):
    if msg:
        await ctx.send(' '.join(msg))
    else:
        await ctx.send("מעוך רצח")


@bot.command(name='aliases', aliases=['a'], help='Sends all the aliases of the given command.')
async def aliases(ctx, message: str):
    try:
        command = commands.Bot.get_command(bot, message)

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


@bot.command(name='repeat', help='Repeats your message.')
async def repeat(ctx, *msg):
    if msg:
        await ctx.send(' '.join(msg))
    else:
        await ctx.send("מעוך רצח")


@bot.command(name='joke', aliases=['y', 'yoyo', 'yoyojokes'], help='Gives you an awesome joke.')
async def send_joke(ctx, cat: str = None):
    try:
        jokes_dict = json.loads(open(PATH + r'\jokes\dict.json', 'r').read())
        jokes_list = list(jokes_dict)

        if cat not in jokes_list and cat:
            await ctx.send('קטגוריה מגניבה אבל אין לי בדיחות כאלה :cry:')
            return

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


@bot.command(name='retardmode', aliases=['retard', 'rm', 'rmode'], help="Unleash the Yoyo's full power.")
async def retard_command(ctx, mode):
    # TODO: Finish command
    global retard_mode

    # TODO: Add more aliases later
    on_aliases = ['on', 'start', 'unleash', 'fullpower']
    off_aliases = ['off', 'stop', 'destroy']

    if mode in on_aliases:
        await ctx.send('בטוח?')
        await time.sleep(2)
        await ctx.send('סתם לא אין חרטות')
        await ctx.send('Unleashing full power...')
        await time.sleep(2)
        await ctx.send('הופההההההההההה!!!! :kissing_smiling_eyes: :rage: :wink: :smiley: :nerd: '
                       ':face_with_symbols_over_mouth: :relaxed::kissing_closed_eyes: :face_with_monocle: '
                       ':heart_eyes: :sunglasses: :sob: :flushed: :kissing_closed_eyes: :face_with_monocle: '
                       ':heart_eyes: :sunglasses: :face_with_symbols_over_mouth: :scream: :astonished: :hugging: '
                       ':grimacing: :money_mouth: :dizzy_face: :cold_face: :hot_face: :exploding_head: :nerd: '
                       ':face_with_symbols_over_mouth: :kissing_closed_eyes: :face_with_monocle: :heart_eyes: '
                       ':sunglasses::scream: :astonished: :hugging: :grimacing: :money_mouth: :dizzy_face:')
        retard_mode = True

    if mode in off_aliases:
        await ctx.send('חחח ניסיון יפה')
        await time.sleep(10)
        await ctx.send('טוב נו...')
        retard_mode = False


bot.run(TOKEN)
