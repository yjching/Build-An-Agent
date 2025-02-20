import requests
import re
import json

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