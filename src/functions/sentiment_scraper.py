# Scrap bodies of text from CNN websites/urls
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrape_cnn(html):
    link = urlopen(html).read()
    soup = BeautifulSoup(link, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()    
    # get text
    text = soup.find_all("div",{"class":"zn-body__paragraph"})
    return ''.join(i.text for i in text)

# text = scrape_cnn("https://www.cnn.com/2021/05/03/us/alleged-kevin-spacey-victim-suit/index.html")
# print(text)
