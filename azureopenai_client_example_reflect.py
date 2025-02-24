import re
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=".env")

from clients.azure_openai import AzureOpenAIClient
from tools.main import calculate, wikipedia

base_client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = ""
)

eval_client = AzureOpenAIClient(
        api_key = os.getenv("azure_openai_key"), 
        endpoint = "ssayjc.openai.azure.com",
        deployment_name="ssayjc-gpt-4o",
        api_version="2024-08-01-preview",
        system_prompt=""
)

from strategies.reflection import ReflectionStrategy

agent = ReflectionStrategy(base_client, eval_client)
agent.run("Which knock knock joke that you wrote for Camille is your favourite?")
