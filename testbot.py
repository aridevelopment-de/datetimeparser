import os
import sys
import traceback

from discord import Embed, Intents
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands.context import Context
from dotenv import load_dotenv
from datetimeparser import parse as p

load_dotenv()

client = Bot(
    command_prefix=when_mentioned_or("+"),
    case_insensitive=True,
    intents=Intents.all()
)


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


@client.command(
    name="parse",
    aliases=["p"],
    description="This command can be used to translate a string into a datetime-object",
    brief="Translate a string into a datetime-object"
)
async def parse(ctx: Context, *, datetime_string: str):

    color = 0x00FF00
    result = None

    try:
        res = p(datetime_string)
        result = f"```python\nfrom datetimeparser import parse\n\nparse(\"{datetime_string}\")```\n```mkd\n# {res}```"
    except:  # noqa
        result = get_latest_stacktrace()
        color = 0xFF0000
    finally:
        embed = Embed(title="Parsed datetime object", color=color, description=f"{result}")
        embed.add_field(
            name="GitHub Repository",
            value="https://github.com/aridevelopment-de/datetimeparser"
        )
        await ctx.reply(embed=embed)


client.run(os.environ["TOKEN"])
