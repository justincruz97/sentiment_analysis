# Scrap bodies of text from CNN websites/urls
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrape_cnn(html):
    """
    Scrape text from a CNN article 

    Args:
        - html (str): html link of a CNN article
    
    Returns:
        - text (str): body of text extracted from the CNN article
    """
    link = urlopen(html).read()
    soup = BeautifulSoup(link, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()    
    # get text
    text = soup.find_all("div",{"class":"zn-body__paragraph"})
    return ''.join(i.text for i in text)