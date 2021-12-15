from bs4 import BeautifulSoup
import urllib.parse
import requests
import time
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def search(q):
  driver = webdriver.Chrome()
  session = HTMLSession()
  url = f"http://duckduckgo.com/?q={urllib.parse.quote(q)}&t=h_&iar=images&iax=images&ia=images"
  driver.get(url)
  wait = 1
  time.sleep(wait)
  #page.html.render(retries=1,wait=1)
  content = driver.page_source
  print(content)
  soup = BeautifulSoup(content, 'html.parser')
  tiles = soup.find_all("div", class_="has-detail")
  imgs = [{"image": urllib.parse.unquote(i.find("div", class_="tile--img__media").find("span").find("img")["src"].split("//external-content.duckduckgo.com/iu/?u=")[1]), "title": i.find("a", class_="tile--img__sub").find("span", class_="tile--img__title").text, "url": i.find("a", class_="tile--img__sub")["href"]} for i in tiles]
  return imgs

if __name__ == "__main__":
  test = search("test")
  print(test)