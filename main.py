import os

from dotenv import load_dotenv

import asyncio

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
    await asyncio.to_thread(plotSingle)
    await message.channel.send("Done ting")

  elif message.content.startswith(".foot radar test"):
      await message.channel.send("Enter season (e.g., 2021-2022):")

      def check(m):
          return m.author == message.author and m.channel == message.channel

      try:
          season_message = await client.wait_for("message", check=check, timeout=60)
          season = season_message.content

          await message.channel.send(f"You entered {season}, {type(season)}")
          
          path="footbot\data\playerReport"+season+".csv"
          df= pd.read_csv(path)

          await message.channel.send(f'''leagues available are\n{list(df["Competition"].unique())}''')

          league_message= await client.wait_for("message",check=check,timeout=60)
          league=league_message.content

          await message.channel.send(f'''You entered {league}, now select position''')

          pos_message= await client.wait_for("message",check=check,timeout=60)
          pos=pos_message.content
          positions={"forward":["FW","MF,FW","FW,MF"],"midfielder":["MF","MF,DF","FW,MF"],"defender":["DF,MF","DF"]}

          temp_df = df[df["Position"].str.contains('|'.join(df[positions[pos]]))]

          await message.channel.send(f'''teams available are\n{list(temp_df["Squad"].loc[temp_df["Competition"]==league].unique())}''')


          team_message = await client.wait_for("message", check=check, timeout=60)
          team=team_message.content

          await message.channel.send(f''' you entered {team}''')


          # Collect other required inputs (position, league, team, player_name) similarly

          # Call the modified plotSingle function with the collected inputs
          
          #await plotSingle(season, position, league, team, player_name)

          await message.channel.send("Done ting")
      except asyncio.TimeoutError:
          await message.channel.send("You took too long to provide input. Command canceled.")

  elif message.content.startswith(".foot math"):
    await message.channel.send(f"1+1 = {1+1}")


  elif message.content.startswith(".foot"):
    await message.channel.send("Hola")

client.run(os.getenv('TOKEN'))

