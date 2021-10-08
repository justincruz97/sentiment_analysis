from sentiment_scraper import scrape_cnn
from sentiment_score_summarizer import summarize_by_score
import requests, json

# Search engine ID: 77e675699531f5abb
# API Key: AIzaSyDmHxFGfkvJWiLIjMG1qAVVOloJhKxGK9M
# Source: https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "AIzaSyDmHxFGfkvJWiLIjMG1qAVVOloJhKxGK9M"

# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "77e675699531f5abb"

def get_articles(query):
    """
    Obtain a list of list of urls based on topic from a query search word

    Args:
        - query (str): specified key word that will be searched within websites
    Return:
        - search_list (list): return a list of url strings from websites
    """
    page = 1
    start = (page-1) * 4 
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data = requests.get(url).json()
    # get the result items
    search_items = data.get("items")
    # iterate over results found
    search_list = []
    for i, search_item in enumerate(search_items, start=1):
        # extract the page url
        link = search_item.get("link")
        search_list.append(link)
    return search_list

def combine_scraped_text(search_list):
    """
    Combine all scraped text from urls in a search_list into one body
    of text

    Args:
        - search_list (list): list of url strings
    Return:
        - combined_text (str): A body of text containing scraped text from url's
    """
    combined_text = []
    for url in search_list:
        url_text = scrape_cnn(url)
        combined_text.append(url_text)
    return combined_text

def build_knowledge_lake(query):
    """
    Create json formatted lists of extracted text from a query

    Args:
        - query (str): user inputted query for Google to search

    Return:
        - Create two files in directory:
            - knowledge_list.json : extracted text in a list, json format
            - knowledge_lake.json : extracted text in json format
    """

    # 1. Get url's related to query search & store them in a list.
    url_list = get_articles(query)
    
    # 2. Gather text from all url's, store them in a list, and clean the spacing.
    combined_text_list = combine_scraped_text(url_list)
    combined_text_list = [x for x in combined_text_list if x != ""]
    
    # 3. Take all bodies of text, and transfer them into json format in same directory.
    # save into giant list, json format
    with open('knowledge_list.json', 'w', encoding='utf-8') as f:
        json.dump(combined_text_list, f, ensure_ascii=False, indent=4)
    # save into json format
    with open('knowledge_lake.json', 'w', encoding='utf-8') as f:
        json.dump(".".join(combined_text_list), f, ensure_ascii=False, indent=4)

def summarize_text():
    with open('knowledge_list.json', 'r',encoding="utf-8" ) as fp:
        data_list = json.load(fp)
    summary = []
    # Summarize with Sentence Scoring
    for i in data_list:
        # print(i)
        lst = summarize_by_score(i)
        summary.append(lst)
    # with open('summary_by_score.json', 'w', encoding='utf-8') as f:
    #     json.dump(summary, f, ensure_ascii=False, indent=4)
    for j in summary:
        print(j)
        print(" ")

def main():
    # step 1
    get_articles("DogeCoine")
    # step 2
    summarize_text()


if __name__ == "__main__":
    main()