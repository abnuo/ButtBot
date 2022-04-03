import shlex, subprocess
import copy
import discord
import discord.utils
from discord.ext import commands
from urllib.parse import unquote
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os
import ast
import asyncio
import websockets
import aiofiles
from concurrent.futures import ProcessPoolExecutor
import time
import sys
import glob
import random
import tracery
import requests
import imgur as imgurl
import json
import itertools
import string
import markovify
import duckduckgo
from tracery.modifiers import base_english
from github import Github

config = json.loads(open("config.json", "r").read())
summonword = "buttbot"
talkclass = 836649499089698816
gpt2tc = "C:\gpt2tc-2021-04-24-win64"
token = config["token"]
heroku = True
msglist = []
msglistwa = []
statesize = 1
memeybear = ["Thicc", "Chonky", "Big", "Lil"]
memeygummy = ["Bonkus", "Yeetus", "Yeezus", "Bingus", "Chungus", "Fingus"]
templatesy = [
    "MeAlsoMe", "ItsRetarded", "Headache", "ItsTime", "ClassNote", "NutButton",
    "Pills", "Balloon", "Classy", "Cola", "Loud", "Milk", "Finally", "Cliff"
]
rules = {
    'origin': ['(WATCHING)your #funny# #wario#!!', "(PLAYING)#games#", "(STREAMING)#videos#", "(WATCHING)my new friend #nametypes# dab"],
    'funny': ['butt', 'ass', 'asshole', 'voidling oc'],
    'wario': ['poop', 'fart', 'yeet', 'fite'],
    'games': ['Voidling Collecters :3', 'Fite #who.capitalize#!'],
    'who': ['coyyy', 'meeed', 'mimlo', 'queddd', 'boohaloo', 'jimy'],
    'videos': ['https://www.youtube.com/watch?v=I8Wf0u8dTWA', 'https://www.youtube.com/watch?v=doWx1vSG22Y', 'https://www.youtube.com/watch?v=rBhbxVmolTE', 'https://www.youtube.com/watch?v=yRUhxFOf_6k', 'https://www.youtube.com/watch?v=lZP41xZ8sjM', 'https://www.youtube.com/watch?v=tw8zVld9OIA', 'https://www.youtube.com/watch?v=oquojYZUL7U', 'https://www.youtube.com/watch?v=F5Vp31IKlik', 'https://www.youtube.com/watch?v=F0htFTcXlCg', 'https://www.youtube.com/watch?v=AFGneaOt9bM'],
    'c': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
    'nametypes': ['#c##c##c##c#', '#c##c##c# the #BOIS# Stan#c##c##c#', '#BOIS#SuperFan#c##c##c##c#'],
    'BOIS': ['Meeed', 'Mimlo', 'Coyoboyo', 'DankyBoi', 'Shmlorp', 'Fruccus', 'Brappus', 'Jimy', 'Grantlogan', 'WSB', 'Mario', 'Wario', 'Spongebob', 'Chutnus']
}
if heroku == True:
  p = subprocess.Popen(["python", "server.py"])
  g = Github(os.environ["gtoken"])
  brainrepo = g.get_repo("abnuo/buttbots-brain")
  contents = brainrepo.get_contents("corpus.txt")
  with open("corpus.txt","rb",encoding="utf-8") as f:
    f.write(contents.decoded_content)
grammar = tracery.Grammar(rules)
#gis = GoogleImagesSearch(config["search_api_key"], config["search_cx"])
grammar.add_modifiers(base_english)
bot = commands.Bot(command_prefix='f!')

def genString(length):
	return ''.join(random.choice(string.ascii_letters) for i in range(length))

def comb(l):
     yield from itertools.product(*([l] * 3))

def buildEmbed(query,alt,image,url,page,pages,author):
  return discord.Embed(title=alt, url=url, description=url, color=discord.Color.blue()).set_author(name=author.name,icon_url=author.avatar_url).set_footer(text="Page "+str(page)+"/"+str(pages)).set_image(url=image)
 
async def hello():
    async with websockets.connect(host) as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

@bot.event
async def on_ready():
    print("I AM ALIVE")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = message.content
    if msg.lower().startswith(summonword) and not msg.lower() == summonword:
      if msg[len(summonword)] == " ":
        msg = msg[len(summonword)+1:len(msg)]
      else:
        msg = msg[len(summonword):len(msg)]
    with open("corpus.txt", "a+", encoding="utf-8") as f:
        f.write(msg + " ")
        newcontents = f.read()
    if heroku == True:
      contents = brainrepo.get_contents("corpus.txt")
      brainrepo.update_file(contents.path,str(time.time()),newcontents,contents.sha)
    with open("corpus.txt", "r", encoding="utf-8") as f:
        text = f.read()
    text_model = markovify.Text(text, state_size=statesize, well_formed=False)
    text_model = text_model.compile()
    if message.channel.id == talkclass:
        changel = bot.get_channel(talkclass)
        await changel.send(str(text_model.make_short_sentence(random.randint(50, 280))))
    if message.content.lower().startswith("buttbot") == True:
        chanle = bot.get_channel(message.channel.id)
        but = message.content.split()
        try:
            seed = but[random.randint(1, len(but) - 1)]
            await chanle.send(' '.join(str(text_model.make_sentence_with_start(seed)).split()[0:random.randint(5, 15)]))
        except:
            await chanle.send(str(text_model.make_short_sentence(random.randint(50, 280))))
    await bot.process_commands(message)

@bot.command()
async def combs(ctx, str):
    for i in comb(str):
        await ctx.send(str(i))

@bot.command()
async def scratch(ctx, user):
  url = f'https://api.scratch.mit.edu/users/{user}'
  print(url)
  r = requests.get(url)
  jsony = json.loads(r.text)
  fart = jsony["profile"]
  bio = fart["bio"]
  status = fart["status"]
  avatar = fart["images"]["90x90"]
  avatar = avatar.replace("png", "gif")
  if bio == "":
    bio = "[Blank]"
  if status == "":
    status = "[Blank]"
  try:
    embed=discord.Embed(color=0xff7f00)
    embed.set_author(name=f'{user}', url=f'https://scratch.mit.edu/users/{user}', icon_url=avatar)
    embed.add_field(name="About me", value=bio, inline=False)
    embed.add_field(name="What I'm working on", value=status, inline=False)
    await ctx.send(embed=embed)
  except Exception as e:
    await ctx.send('Free Error: ' + str(e))

@bot.command()
async def tracery(ctx):
	await ctx.send(grammar.flatten("#origin#"))
@bot.command()
async def updoot(ctx, id):
  massage = await ctx.fetch_message(id)
  await massage.add_reaction('<:updoot:763716527203549194>')
  await ctx.send('Updooted!')
@bot.command()
async def react(ctx, emoji, id):
  massage = await ctx.fetch_message(id)
  await massage.add_reaction(emoji)
  await ctx.send('i did it B O I')
@bot.command()
async def u8(ctx, data):
  filename = 'u8_' + genString(5)
  if ctx.message.attachments:
      r = requests.get(ctx.message.attachments[0].url)
      os.system('echo ' + r.text + ' | ffmpeg -f u8 -ar 8000 -ac 1 -i - ' + filename + '.wav')
  elif data.startswith('http://') or data.startswith('https://'):
      #r = requests.get(data)
      os.system('ffmpeg -f u8 -ar 8000 -ac 1 -i ' + data + ' ' + filename + '.wav')
  else:
      await ctx.send('Bruh There No TEXT Or URL')
  try:
      await ctx.send(file=discord.File(filename + '.wav'))
  except Exception as e:
      await ctx.send('Fail: ```' + str(e) + '```')
  #await ctx.send(file=discord.File(filename + '.wav'))
@bot.command()
async def tou8(ctx, data):
  filename = 'u8_' + genString(5)
  if ctx.message.attachments:
      r = requests.get(ctx.message.attachments[0].url)
      os.system('ffmpeg -i ' + ctx.message.attachments[0].url + ' -f u8 -ar 8000 -ac 1 ' + filename + '.raw')
  elif data.startswith('http://') or data.startswith('https://'):
      os.system('ffmpeg -i ' + data + ' -f u8 -ar 8000 -ac 1 ' + filename + '.raw')
  else:
      await ctx.send('Bruh There No ATTACHMENT Or URL')
  try:
      await ctx.send(file=discord.File(filename + '.raw'))
  except Exception as e:
      await ctx.send('Fail: ```' + str(e) + '```')
@bot.command()
async def compress(ctx, msg):
  with open("corpus.txt", "r", encoding="utf-8") as f:
    splitText = f.read().split(" ")
  splitMsg = ctx.message.content.split(bot.command_prefix + sys._getframe().f_code.co_name + " ")[1].split(" ")
  compressed = []
  for i in splitMsg:
    if i in splitText:
      compressed.append(chr(splitText.index(i)+1000))
    else:
      await ctx.send("What Does " + i + " Mean?")
  await ctx.send("".join(compressed))
@bot.command()
async def decompress(ctx, msg):
  with open("corpus.txt", "r", encoding="utf-8") as f:
    splitText = f.read().split(" ")
  chars = [ord(i) for i in msg]
  decompressed = []
  for i in chars:
    indexy = i-1000
    if indexy < len(splitText):
      decompressed.append(splitText[indexy])
  await ctx.send(" ".join(decompressed))
@bot.command()
async def echo(ctx):
  m = ctx.message.content.split(bot.command_prefix + sys._getframe().f_code.co_name + " ")[1]
  await ctx.send(m)
@bot.command()
async def complete(ctx):
  msg = ctx.message.content.split(bot.command_prefix + sys._getframe().f_code.co_name + " ")[1]
  await ctx.send("Generating...")
  completed = os.popen(f"cd {gpt2tc} & gpt2tc g \"" + msg + "\"").read()
  await ctx.send(completed)
@bot.command()
async def imgur(ctx):
  
  image = imgurl.genurls(5,1,'')[0]

  editmsg = await ctx.send(str(image))
  
  def check(m: discord.Message):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
  while True:
    try:
      msg = await bot.wait_for(event = 'message', check = check, timeout = 30.0)
    except asyncio.TimeoutError:
      return
    else:
      if msg.content == "n":
        image = imgurl.nextUrl(image)
        await editmsg.edit(content=str(image))
        await msg.delete()
      elif msg.content == "b":
        image = imgurl.prevUrl(image)
        await editmsg.edit(content=str(image))
        await msg.delete()
      elif msg.content == "r":
        image = imgurl.genurls(5,1,'')[0]
        await editmsg.edit(content=str(image))
        await msg.delete()
@bot.command()
async def img(ctx):
  query = ctx.message.content.split(bot.command_prefix + sys._getframe().f_code.co_name + " ")[1]
  author = ctx.message.author
  fetchmsg = await ctx.send("Fetching images...")
  images = duckduckgo.search(query)
  imagen = 0
  imagem = len(images)
  image = images[imagen]
  embed = buildEmbed(query,images[imagen]["title"],images[imagen]["image"],images[imagen]["url"],imagen,imagem,author)
  fetchmsg.delete()
  editmsg = await ctx.send(embed=embed)
  
  def check(m: discord.Message):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
  while True:
    try:
      msg = await bot.wait_for(event = 'message', check = check, timeout = 30.0)
    except asyncio.TimeoutError:
      return
    else:
      if msg.content == "n":
        imagen = imagen+1
        image = images[imagen]
        embed = buildEmbed(query,images[imagen]["title"],images[imagen]["image"],images[imagen]["url"],imagen,imagem,author)
        await editmsg.edit(embed=embed)
        await msg.delete()
      elif msg.content == "b":
        imagen = imagen-1
        image = images[imagen]
        embed = buildEmbed(query,images[imagen]["title"],images[imagen]["image"],images[imagen]["url"],imagen,imagem,author)
        await editmsg.edit(embed=embed)
        await msg.delete()
      elif msg.content == "r":
        imagen = random.randint(0,len(images)-1)
        image = images[imagen]
        embed = buildEmbed(query,images[imagen]["title"],images[imagen]["image"],images[imagen]["url"],imagen,imagem,author)
        await editmsg.edit(embed=embed)
        await msg.delete()
@bot.command()
async def download(ctx):
  url = ctx.message.content.split(bot.command_prefix + sys._getframe().f_code.co_name + " ")[1]
  fn = genString(5)
  await ctx.send("Downloading video...")
  process = os.popen(f"yt-dlp {url} -o download/{fn}.mkv")
  preprocessed = process.read()
  process.close()
  merged = glob.glob(f"download/{fn}.*")[0]
  await ctx.send("Resizing...")
  if os.path.getsize(merged) > 8000000:
    process = os.popen(f"ffmpeg -i {merged} -preset veryslow -t 10 download/{fn}.mp4")
  else:
    process = os.popen(f"ffmpeg -i {merged} -preset veryslow download/{fn}.mp4")
  preprocessed = process.read()
  process.close()
  await ctx.send(file=discord.File(f"download/{fn}.mp4"))
  os.remove(merged)
  os.remove(f"download/{fn}.mp4")

bot.run(token)
