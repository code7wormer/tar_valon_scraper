import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url="https://library.tarvalon.net/index.php?title=The_Eye_of_the_World:_Chapter_Summaries"
def list_scrape(url):
  headers = {
      "User-Agent": "TarValonScraper/0.1"
    }
  
  response = requests.get(
      url,
      headers=headers,
      timeout=10
  )
  soup=BeautifulSoup(response.text,"html.parser")
  content=soup.find(id="mw-content-text")
  chapters={}
  for child in content.find_all("li"):
    link=child.find("a")
    chapter_name=link.get_text(" ",strip=True)
    chap_rel_link=link.get("href")
    chap_url=urljoin(url,chap_rel_link)
    chapters[chapter_name]=chap_url
  return chapters
