import re
import os
os.getcwd()
import requests
import json
import httpx
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path="Build-An-Agent/.env")

from clients.main import hello_world
from clients.azure_openai import AzureOpenAIClient
# from clients.ollama import OllamaClient
hello_world()

system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

Example session:
Question: What is the capital of China?
Thought: I should look up China on Wikipedia.
Action: wikipedia: China
PAUSE

You will be called again with this:

Observation: China is a country. The capital is Beijing.

You then output:

Answer: The capital of China is Beijing.
""".strip()

client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = system_prompt
)

def calculate(what):
    return eval(what)

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]

def run_agent(client, question, no_times):
    known_actions = {
        "wikipedia": wikipedia,
        "calculate": calculate,
    }
    i = 0
    # Define the regular expression pattern
    action_re = re.compile(r'Action:\s*(\w+)\s*:\s*(.*)')
    next_prompt = question
    while i < no_times:
        i+=1
        result = client.generate_completion(next_prompt)
        print(i)
        print(result)
        # Search for the pattern in the input string
        actions = [action_re.search(a) for a in result.split('\n') if action_re.search(a)]
        # Check if a match was found and extract the captured group
        if actions:
            action, action_input = actions[0].groups()
            cleaned_string = action_input.replace("PAUSE", "").strip()
            observation = known_actions[action](cleaned_string)
            next_prompt = "Observation: {}".format(observation)
            print(next_prompt)
        else:
            return

question = "5 ** 3"
run_agent(client, question, 2)

question = "Where is SAS Institute located?"
run_agent(client, question, 5)

def run_agent_v2(client, question, no_times):
    known_actions = {
        "wikipedia": wikipedia,
        "calculate": calculate,
    }
    i = 0
    # Define the regular expression pattern
    action_re = re.compile(r'Action:\s*(\w+)\s*:\s*(.*)')
    next_prompt = question
    while i < no_times:
        i+=1
        result = client.generate_completion(next_prompt)
        print(i)
        print(result)
        # Search for the pattern in the input string
        actions = [action_re.search(a) for a in result.split('\n') if action_re.search(a)]
        # Check if a match was found and extract the captured group
        if actions:
            action, action_input = actions[0].groups()
            cleaned_string = action_input.replace("PAUSE", "").strip()
            observation = known_actions[action](cleaned_string)
            next_prompt = question+" Observation: {}".format(observation)
            print(next_prompt)
        else:
            return
        # return

question = "Where is SAS institute?"
run_agent_v2(client, question, 5)



def wikipedia_test(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()
wikipedia_test("SAS Institute")