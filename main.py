# bot works only in polish language.
# Pard Corp.

import discord
from discord.ext import commands
import tokens
import json
import io
import aiohttp

main_fp = 'replace_servers.json'

def seek_and_truncate(file: io.TextIOWrapper):
    file.seek(0)
    file.truncate()

bot = commands.Bot("?", intents=discord.Intents.all())

@bot.hybrid_command(name="change", help="zmien dzialanie bota (tak / nie)")
async def change(ctx: commands.Context, option: str): # tak / nie
   if (option == "tak"):
      with open(main_fp, 'r+') as servers:
          content = json.load(servers)
          content[str(ctx.guild.id)] = True
          seek_and_truncate(servers)
          json.dump(content, servers)
          await ctx.reply("ok.")
   elif (option == "nie"):
      with open(main_fp, 'r+') as servers:
          content = json.load(servers)
          content[str(ctx.guild.id)] = False
          seek_and_truncate(servers)
          json.dump(content, servers)
          await ctx.reply("ok.")
   else:
      await ctx.reply("zla opcja! wybierz jedno pomiedzy; **tak**, **nie**.")               

@bot.event
async def on_message(message: discord.Message):
   if (message.author == bot.user):
     return
   with open(main_fp, 'r') as servers: # i know this is very inefficient, but i don't have an idea how to do that in other way.
      content = json.load(servers)
      if str(message.guild.id) in content:
        if content[str(message.guild.id)]:
         webhooks = await message.channel.webhooks()
         mapped_webhooks = map(lambda x: x.name, webhooks)
         if not "Replacer System" in mapped_webhooks:
          await message.channel.create_webhook(name="Replacer System")
         else:
          for webhook in webhooks:
           if webhook.name == "Replacer System":
            url = webhook.url
            break   
          async with aiohttp.ClientSession() as session:
           client = discord.Webhook.from_url(url, session=session)
           message_content = message.content
           pattern = {
            ".": " **[kropka]** ",
            ",": " **[przecinek]** ",
            ":": " **[dwukropek]** ",
            ";": " **[średnik]** ",
            "-": " **[myślnik]** ",
            "_": " **[podłoga]** ",
            "?": " **[pytajnik]** ",
            "!": " **[wykrzyknik]** ",
            "/": " **[ukośnik]** ",
            "\\": " **[backslash]** ",
            "@": " **[małpa]** ",
            "#": " **[hashtag]** ",
            "$": " **[dolar]** ",
            "%": " **[procent]** ",
            "^": " **[potęga]** ",
            "&": " **[i]** ",
            "(": " **[otwierający nawias]** ",
            ")": " **[zamykający nawias]** ",
            # i can't add the "*" sign, because of bolding
           }
           for key, value in pattern.items():
             message_content = message_content.replace(key, value)
           if (message_content != message.content):   
            if (message.author.id != client.id):
             await message.delete()
             name = message.author.global_name if message.author.global_name else message.author.name
             await client.send(message_content, username=name, avatar_url=message.author.avatar)
            else:
             return 
           else:
            return  
   await bot.process_commands(message)      

bot.run(tokens.PUNCTUACTION_BOT.token)           
