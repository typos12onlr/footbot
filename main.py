import os

from dotenv import load_dotenv

import discord

from utils.footbotgetdata import *

from utils.footbotradar import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
@client.event
async def on_ready():
  print("Visca Barca")


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith(".foot sync data"):
    await message.channel.send(f"Updating Dataset")
    i = "2023-2024"
    makeDataset(i)
    await message.channel.send(f"Updated Dataset")

  elif message.content.startswith(".foot Real Madrid"):
    await message.channel.send("Madrid cabron, saluda al campeon")

  elif message.content.startswith(".foot Barcelona"):
    await message.channel.send(
        "O le le, O la la, Ser del Barca es, el mas  millor que hi ha")
  elif message.content.startswith(".foot radar"):
    await plotSingle()
    await message.channel.send("Done ting")
  elif message.content.startswith(".foot"):
    await message.channel.send("Hola")


client.run(os.getenv('TOKEN'))
