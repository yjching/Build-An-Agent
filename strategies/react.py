from strategies.tool import SingleToolStrategy

class ReActStrategy(SingleToolStrategy):
    def __init__(self, base_client, tools_list):
        super().__init__(base_client, tools_list)
