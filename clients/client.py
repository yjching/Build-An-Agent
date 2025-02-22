from typing import Optional

def hello_world():
    print("Hello World")

class BaseClient:
    def __init__(self, system_prompt = ""):
        self._system_prompt = system_prompt
        self.response = None
        self.conversation_memory = None

        self.init_conversation_memory()

    @property
    def system_prompt(self):
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value):
        self._system_prompt = value
        ## TODO: Changing system_prompt resets memory
        self.init_conversation_memory()
    
    def init_conversation_memory(self):
        self.conversation_memory = [
            {"role": "system", "content": f"{self.system_prompt}"}
        ]

    def create_prompt_from_string(self, prompt):
        self.conversation_memory.append(
            {"role": "user", "content": f"{prompt}"}
        )
        return self.conversation_memory