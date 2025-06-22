import discord
import logging
import asyncio
from config import DISCORD_TOKEN
from llm_manager import AnythingLLMManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
client = discord.Client(intents=intents)
llm = AnythingLLMManager()

@client.event
async def on_ready():
    logging.info(f"Bot ready: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user or not isinstance(message.channel, discord.DMChannel):
        return

    snippet = message.content[:200] + ("..." if len(message.content) > 200 else "")
    logging.info(f"Message from {message.author.id}: {snippet}")
    async with message.channel.typing():
        reply = await llm.send_message_to_thread(message.author.id, message.content)

    if len(reply) > 2000:
        for i in range(0, len(reply), 2000):
            await message.reply(reply[i:i+2000])
    else:
        await message.reply(reply)

if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logging.info("Shutting down.")
        asyncio.run(client.close())
