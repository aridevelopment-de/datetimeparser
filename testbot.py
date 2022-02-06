import os
import sys
import traceback

import discord
from dotenv import load_dotenv
from datetimeparser import parse

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)


# https://discord.com/oauth2/authorize?client_id=939862584935477298&scope=bot&permissions=0

def get_latest_stacktrace():
    # Helper function for retrieving the latest stacktrace
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]

    if exc is not None:
        del stack[-1]

    trc = 'Traceback (most recent call last):\n'
    stack_str = trc + ''.join(traceback.format_list(stack))

    if exc is not None:
        stack_str += ' ' + traceback.format_exc().lstrip(trc)

    return stack_str


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(message):
    if message.content.startswith("!parse "):
        datetime_string = message.content.split("!parse ")[1]

        color = 0x00FF00
        result = None

        try:
            result = parse(datetime_string)
            result = f"```python\nfrom datetimeparser import parse\n\nparse(\"{datetime_string}\")```\n```mkd\n# {result}```"
        except:  # noqa
            result = get_latest_stacktrace()
            color = 0xFF0000
        finally:
            embed = discord.Embed(title="Parsed datetime object", color=color, description=f"{result}")
            await message.channel.send(embed=embed)


client.run(os.environ["TOKEN"])
