from clients.base import BaseClient

class ReflectionStrategy():
    def __init__(self, base_client, eval_client):
        self.base_client = base_client
        self.eval_client = eval_client
    @property
    def clients(self):
        return self._clients

    @clients.setter
    def clients(self, value):
        self._clients = value
    
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
            print(f"Responder: I will send this to the evaluator")
            ## Save to client memory
            evaluation_of_response = self.eval_client.generate_completion(response)
            print(f"Evaluator: My evaluation is {evaluation_of_response}")
            ## Save to evaluation memory
            if "<OK>" in evaluation_of_response:
                print("Stop reflection loop.")
                break
            else: 
                question = response
        return response
