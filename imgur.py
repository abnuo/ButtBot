import random
import hashlib
import requests
import glob
import os
import sys
import imghdr
import base62
import __main__

downfolder = 'images/'
failures = 0
suffixes = ["_d", "s", ""]
#urlformat = "https://i.imgur.com/{0}{1}.png"
urlformat = "https://abnuosite.herokuapp.com/imgurproxy.php?id={0}{1}"
removedhash = "9b5936f4006146e4e1e9025b474c02863c0b5614132ad40db4b925a10e8bfbb9"

def rand(byte):
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  if byte == 5:
    byter = 5
  elif byte == 7:
    byter = 7
  return ''.join(random.choice(letters) for i in range(byte))

def genurls(byte, amount, urlsuffix):
  global failures
  failures = 0
  imgururls = []
  if not urlsuffix in suffixes:
    print('Not a valid URL suffix, using "_d"')
    urlsuffix = '_d'
  try:
    for i in range(amount):
      while True:
        randerps = rand(byte)
        url2 = urlformat.format(randerps,urlsuffix)
        r = requests.get(url2)
        if hashlib.sha256(r.content).hexdigest() != removedhash:
          imgururls.append(url2)
          break
    return imgururls
  except Exception as e:
    print('Error.', str(e))
def nextUrl(url):
  id = url.split("https://i.imgur.com/")[1].replace(".png","")
  decodedId = base62.decode(id)
  newId = base62.encode(decodedId+1)
  return "https://i.imgur.com/"+newId+".png"
def prevUrl(url):
  id = url.split("https://i.imgur.com/")[1].replace(".png","")
  decodedId = base62.decode(id)
  newId = base62.encode(decodedId-1)
  return "https://i.imgur.com/"+newId+".png"
def downloadurls(listor):
  files = glob.glob(downfolder + '*.*')
  for i in files:
    if i == __file__:
      print('Skipping current script.')
    else:
      os.remove(i)
  print('Downloading urls.')
  for i in range(len(listor)):
    try:
      r = requests.get(listor[i])
      filetype = imghdr.what(None, h=r.content)
      if filetype == None:
        print('Filetype unidentifiable, using png')
        filetype = "png"
      with open(downfolder + listor[i].split(urlformat.format("",""))[1].split(".png")[0] + '.' + filetype, 'wb') as image:
        image.write(r.content)
    except Exception as e:
      print('Error downloading image url', str(i), str(e))

if __name__ == "__main__":
  args = sys.argv
  if args[1] == "-d":
    urls = genurls(5, int(args[2]), '')
    print(urls)
    downloadurls(urls)
  else:
    urls = genurls(5, int(args[1]), '')
    for i in urls:
      print(i)
