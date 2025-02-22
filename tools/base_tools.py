import httpx
import requests
from typing import Optional

def calculate(what):
    return eval(what)

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def get_space_news(n_articles: int = 5):
    summarised_content = ""
    headers = {"Accept": "application/json"}
    get_space_news_request = requests.get(
        url = f"https://api.spaceflightnewsapi.net/v4/articles?limit={n_articles}",
        headers=headers
    )
    output_response = get_space_news_request.json()

    for i, item in enumerate(output_response['results'], 1):
        summarised_content = summarised_content + f"Story {i}: "+item['summary']+' '

    return summarised_content