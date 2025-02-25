'''
Pattern 1
Evaluator LLM evaluates response from initial responder and iterates until sufficient.
'''

from strategies.base_strategy import BaseStrategy

class ReflectionStrategy(BaseStrategy):
    def __init__(self, base_client, eval_client):
        super().__init__(base_client)
        self.eval_client = eval_client
    def run(self, question, n_iter: int = 10):
        self.eval_client.system_prompt = f"""Evaluate how good the following response is, given the question. If the response ise poor, respond with your evaluation on what to improve with the response.
        If the response is good and does not need changes, append the following to the end of your response: <OK>. 
        Question: {question}.
        Response: """
        step = 0
        while step < n_iter:
            step+=1
            response = self.base_client.generate_completion(question)
            print(f"Responder: My initial response is: {response}")
            print("Responder: I will send this to the evaluator")
            ## Save to client memory
            evaluation_of_response = self.eval_client.generate_completion(response)
            print(f"Evaluator: My evaluation is {evaluation_of_response}")
            ## Save to evaluation memory
            if "<OK>" in evaluation_of_response:
                print("Stop reflection loop.")
                break
            question = response
        return response
