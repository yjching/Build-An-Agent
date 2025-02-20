from typing import Optional
from ollama import chat
from main import BaseClient

class OllamaClient(BaseClient):
    def __init__(self, system_prompt:str, model_name:str):
        super().__init__(system_prompt)
        self.model = model_name