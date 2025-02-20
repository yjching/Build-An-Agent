from typing import Optional

def hello_world():
    print("Hello World")

class BaseClient:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.response = None
    
    def create_prompt_from_string(self, prompt):
        messages = [
            {"role": "system", "content": f"{self.system_prompt}"},
            {"role": "user", "content": f"{prompt}"}
        ]
        return messages