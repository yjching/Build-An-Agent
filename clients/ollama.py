from typing import Optional
from ollama import chat
from ollama import ChatResponse
from clients.client import BaseClient

class OllamaClient(BaseClient):
    def __init__(self, model_name:str, system_prompt:str):
        super().__init__(system_prompt)
        self.model_name = model_name

    def generate_completion(self, prompt):
        messages = self.create_prompt_from_string(prompt)

        response = chat(self.model_name, messages)
        return response['message']['content']
