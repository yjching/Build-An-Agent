import re
import os
from dotenv import load_dotenv, find_dotenv

from clients.ollama import OllamaClient
from prompts.base_prompts import TOOL_SYSTEM_PROMPT

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=TOOL_SYSTEM_PROMPT
)

import requests
def get_space_news():
    summarised_content = ""
    headers = {
        "Accept": "application/json"
    }
    get_space_news = requests.get(
        url = "https://api.spaceflightnewsapi.net/v4/articles/",
        headers=headers
    )
    output_response = get_space_news.json()

    for i, item in enumerate(output_response['results'], 1):
        summarised_content = summarised_content + f"Story {i}: "+item['summary']+' '

    return summarised_content

base_client.generate_completion("What is the latest news on space?")



