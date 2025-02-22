## Pattern 2
## LLM calls Tool
import re
import json

from tools.base_tools import get_space_news

class SingleToolStrategy():
    def __init__(self, base_client):
        self.base_client = base_client
    @property
    def clients(self):
        return self._clients

    @clients.setter
    def clients(self, value):
        self._clients = value
    
    def set_available_tools(self, tools_list: list):
        available_tools = {}
        for item in tools_list:
            available_tools[item.__name__] = item
        return available_tools
    
    def run(self, prompt, tools_list: list):
        available_tools = self.set_available_tools(tools_list)

        saved_response = self.base_client.generate_completion(prompt)

        ## Parse response for what tool to use
        ## Extract the XMLs, load as JSON and take name and arguments
        ## to call the tool
        pattern = r'</?tool_call>'
        clean_response = re.sub(pattern, '', saved_response)
        parsed_output = json.loads(clean_response)
        # available_tools[parsed_output['name']](**parsed_output['arguments'])
        return available_tools[parsed_output['name']](**parsed_output['arguments'])