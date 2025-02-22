from typing import Optional
from ollama import chat
from ollama import ChatResponse

from main import BaseClient

class OllamaClient(BaseClient):
    def __init__(self, system_prompt:str, model_name:str):
        super().__init__(system_prompt)
        self.model = model_name

    def generate_completion(self, prompt):
        messages = self.create_prompt_from_string(prompt)

        response = chat(self.model_name, messages)
        return response['message']['content']
