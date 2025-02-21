from typing import Optional

def hello_world():
    print("Hello World")

class BaseClient:
    def __init__(self, system_prompt = ""):
        self._system_prompt = system_prompt
        self.response = None
    
    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value):
        self._system_prompt = value

    def create_prompt_from_string(self, prompt):
        messages = [
            {"role": "system", "content": f"{self.system_prompt}"},
            {"role": "user", "content": f"{prompt}"}
        ]
        return messages