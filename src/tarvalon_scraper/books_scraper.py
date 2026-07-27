import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url="https://library.tarvalon.net/index.php?title=Chapter_Summaries"
def book_scrape(url):
  headers = {
    "User-Agent": "TarValonScraper/0.1"
  }

  response = requests.get(
      url,
      headers=headers,
      timeout=30
  )
  soup=BeautifulSoup(response.text,"html.parser")
  content=soup.find(id="mw-content-text")
  books={}
  for child in content.find_all("li"):
    link=child.find("a")
    book_name=link.get_text(" ",strip=True)
    book_rel_link=link.get("href")
    book_url=urljoin(url,book_rel_link)
    books[book_name]=book_url
  return books