from sentiment_scraper import scrape_cnn
# from sentiment_cosine_summarizer import generate_summary_2
from sentiment_score_summarizer import summarize_by_score
import requests, json

# Search engine ID: 77e675699531f5abb
# API Key: AIzaSyDmHxFGfkvJWiLIjMG1qAVVOloJhKxGK9M
# Source: https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
API_KEY = "AIzaSyDmHxFGfkvJWiLIjMG1qAVVOloJhKxGK9M"

# get your Search Engine ID on your CSE control panel
SEARCH_ENGINE_ID = "77e675699531f5abb"

# Search the query
query = "Dogecoin"

def get_urls(query):
    print("IAMHERE --> 1")
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
    # iterate over 10 results found
    search_list = []
    for i, search_item in enumerate(search_items, start=1):
        # get the page title
        title = search_item.get("title")
        # page snippet
        snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        link = search_item.get("link")
        search_list.append(link)
    return search_list

def combine_scraped_text(search_list):
    print("search_list:", search_list)
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

"""
Load json file
with open('fromatted_TextBlob_IMP.json', 'r',encoding="utf-8" ) as fp:
        cl = NaiveBayesClassifier(fp, format="json")

with open('IMP_combined_final_5000_lower.json', 'r',encoding="utf-8" ) as fp:
        TRAINING_DATA = json.load(fp)
"""

def get_articles(query):
    url_list = get_urls(query)
    combined_text_list = combine_scraped_text(url_list)
    combined_text_list = [x for x in combined_text_list if x != ""]

    # dump knowledge lake
    with open('article_sentences.json', 'w', encoding='utf-8') as f:
        json.dump(combined_text_list, f, ensure_ascii=False, indent=4)
    # save into giant list
    # with open('article.json', 'w', encoding='utf-8') as f:
    #     json.dump(".".join(combined_text_list), f, ensure_ascii=False, indent=4)

    # load json file

def summarize_text():
    with open('article_sentences.json', 'r',encoding="utf-8" ) as fp:
        article = json.load(fp)
    summary = []
    # Summarize with Sentence Scoring
    for i in article:
        # print(i)
        lst = summarize_by_score(i)
        summary.append(lst)
    with open('summary_by_score.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)


# step 1
get_articles("DogeCoine")
# step 2
summarize_text()