'''
Pattern 2
LLM calls Tool
'''

import re
import json

from strategies.base_strategy import BaseStrategy

class SingleToolStrategy(BaseStrategy):
    def __init__(self, base_client, tools_list: list):
        super().__init__(base_client)
        self.tools_list = tools_list

    def set_available_tools(self):
        available_tools = {}
        for item in self.tools_list:
            available_tools[item.__name__] = item
        return available_tools
    def run(self, prompt):
        available_tools = self.set_available_tools()

        saved_response = self.base_client.generate_completion(prompt)

        ## Parse response for what tool to use
        ## Extract the XMLs, load as JSON and take name and arguments
        ## to call the tool
        pattern = r'</?tool_call>'
        clean_response = re.sub(pattern, '', saved_response)
        parsed_output = json.loads(clean_response)
        return available_tools[parsed_output['name']](**parsed_output['arguments'])
