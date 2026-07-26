import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url="https://library.tarvalon.net/index.php?title=Chapter_Summaries"
response=requests.get(url)
soup=BeautifulSoup(response.text,"html.parser")
content=soup.find(id="mw-content-text")
books={}
for child in content.find_all("li"):
  link=child.find("a")
  book_name=link.get_text(" ",strip=True)
  book_rel_link=link.get("href")
  book_url=urljoin(url,book_rel_link)
  books[book_name]=book_url
url2="https://library.tarvalon.net/index.php?title=The_Eye_of_the_World:_Chapter_Summaries"#selected book




