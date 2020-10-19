# Join the Discord server we trapped the bot in!
# We'd post it on /r/Ooer but we'd get banned.
# https://discord.gg/pKGBpA

from dotenv import load_dotenv
load_dotenv()

import logging
import os
import json
import random
from utils import Crombed
from discord.ext import commands

import badmarkov

logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO)


failure_phrases = [
    "Wrong.",
    "You have failed.",
    "Incorrect.",
    "no",
    "You utter fool",
    "Fool...",
    "Error!",
    "ERROR:",
    "You have erred.",
    "Imagine writing code that makes this error:",
    "Do you are have dumb?",
    "what!",
    "Bad at computer!",
    "Bad at computer. Bad at computer!",
    "oh no"
]


class OoerBot(commands.AutoShardedBot):
    # i just realized there's basically no reason to subclass but w/e

    async def on_message(self, message):
        if message.author.bot:  # this will catch webhooks as well iirc
            return
        if self.user.mentioned_in(message):
            # await message.channel.send(random.choice(pinged))
            await message.channel.send(self.markov.generate())

        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        embed = Crombed(
            title = random.choice(failure_phrases),
            description = str(exception),
            color_name = "red",
            author = ctx.author
        )
        await ctx.send(embed=embed)


print("Initializing bot...")
bot = OoerBot(
    command_prefix = os.environ["COMMAND_PREFIX"],
    owner_ids = json.loads(os.environ["BOT_OWNERS"]),
    case_insensitive = True
)

bot.logger = logger
bot.markov = badmarkov.AwfulMarkov("markov_ooer", state_size=2)

@bot.event
async def on_ready():
    print("ooo online")

@bot.command()
async def ping(ctx):
    """ Respond with the bot's reponse time. """
    await ctx.send(f"Ping! Took **{round(bot.latency * 1000, 2)}** ms")

extensions = ["jishaku", 'letters', "delphi", "garlic", "asher", "lumien", "invalid"]  # put this... somewhere, later
for extension in extensions:
    try:
        print(f"Loading extension {extension}...")
        bot.load_extension(extension)
        bot.logger.info(f"Loaded extension {extension}")
    except Exception as e:
        bot.logger.error(f"Failed to load extension {extension}; {e}")


print("Logging in...")
bot.run(os.environ["DISCORD_BOT_TOKEN"])
