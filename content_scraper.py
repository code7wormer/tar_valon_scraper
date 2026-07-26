import requests
from bs4 import BeautifulSoup
# url="https://library.tarvalon.net/index.php?title=The_Great_Hunt:_Chapter_3"
def content_scrape(url):
  response=requests.get(url)
  txt=""
  soup=BeautifulSoup(response.text,"html.parser")
  content=soup.find(id="mw-content-text")
  #mw-content-text
  heading = soup.select_one("#firstHeading").get_text(" ", strip=True) +"\n\n"
  txt+=f"# {heading.upper()}"
  first_p = content.find("p")
  if first_p and "Next Chapter" in first_p.get_text():
    first_p.decompose()
  collect=True
  for child in content.find_all(recursive=False):
      if child.get("id")=="toc":
        collect=False
      if child.name=="h2":
        span = child.find("span")
        section = span.get("id") if span else None
        if section=="Outline":
          collect=True
        if section=="Spoilers":
          collect=False
          break
      if collect:
        # txt=txt+child.get_text(" ", strip=True)+"\n\n"
            if child.name == "h2":
                heading = child.get_text(" ", strip=True)
                txt += f"## {heading}\n\n"

            elif child.name == "h3":
                heading = child.get_text(" ", strip=True)
                txt += f"### {heading}\n\n"

            elif child.name == "p":
                txt += child.get_text(" ", strip=True) + "\n\n"

            elif child.name in ["ul", "ol"]:
                for li in child.find_all("li", recursive=False):
                    txt += "- " + li.get_text(" ", strip=True) + "\n"
                txt += "\n"


  return txt
      