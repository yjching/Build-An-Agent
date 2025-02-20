import re
import os
import requests
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path="Build-An-Agent/.env")

class AzureOpenAIClient:
    def __init__(self, api_key, endpoint, deployment_name, api_version, system_prompt):
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version
        self.system_prompt = system_prompt
        self.response = None
    def create_prompt_from_string(self, prompt):
        messages = [
            {"role": "system", "content": f"{self.system_prompt}"},
            {"role": "user", "content": f"{prompt}"}
        ]
        return messages

    def generate_completion(self, prompt):
        messages = self.create_prompt_from_string(prompt)
        
        api_key = self.api_key
        endpoint = f"https://{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"

        # Define the headers
        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }

        # Define the payload
        payload = {
            "messages": messages
        }

        # Make the POST request
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        cleaned_response = re.sub(r'\n+', ' ', response.json()['choices'][0]['message']['content'])
        return cleaned_response

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

Example session:

Question: What is 4 * 5?
Thought: I should calculate using the numbers provided. 
Action: calculate: 4*5
PAUSE

You will be called again with this:

Observation: 4 times 5 is 20.

You then output:

Answer: 20.
""".strip()

client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = system_prompt
)

question = "What is 5 times 3?"

def calculate(what):
    return eval(what)

def run_agent(client, question, no_times):
    known_actions = {
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

run_agent(client, question, 5)
