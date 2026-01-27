import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


# ───────────────────────────────
#  Sync Slash Commands
# ───────────────────────────────
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")


# ───────────────────────────────
#  Load Cogs
# ───────────────────────────────
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())