from strategies.tool import SingleToolStrategy

class ReActStrategy(SingleToolStrategy):
    def __init__(self, base_client, tools_list):
        super().__init__(base_client, tools_list)
    def run(self, question, n_iter: int = 10):
        step = 0
        while step < n_iter:
            step+=1
            saved_response = self.base_client.generate_completion(question)
            