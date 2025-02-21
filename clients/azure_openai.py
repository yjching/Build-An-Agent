import requests
import re
import json

from clients.main import BaseClient

class AzureOpenAIClient(BaseClient):
    def __init__(self, api_key, endpoint, deployment_name, api_version, system_prompt=""):
        super().__init__(system_prompt)
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version

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
        # print(response.json())
        cleaned_response = re.sub(r'\n+', ' ', response.json()['choices'][0]['message']['content'])

        ## Append to memory
        self.conversation_memory.append({
            "role": "assistant",
            "content": cleaned_response
        })
        return cleaned_response