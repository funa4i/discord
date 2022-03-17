import discord
import asyncio
import requests
import mitmproxy
import shutil

resp = requests.get("https://api.thecatapi.com/v1/images/search")
print(resp.json()[0]['url'])
resp2 = requests.get("https://dog.ceo/api/breeds/image/random")
print(resp2.json()["message"])


class YLBotClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        global resp
        if "кошка" in message.content.lower():
            await message.channel.send(resp.json()[0]['url'])
        if "rickrolled" in message.content.lower():
            await message.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        if "собака" in message.content.lower():
            await message.channel.send(resp2.json()["message"])


TOKEN = "OTU0MDE3NTEzNTA1NzEwMTYx.YjNADA.DQigjXtYAZElNk28nOQ3kW2VZkQ"
client = YLBotClient()

client.run(TOKEN)
