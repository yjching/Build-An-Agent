import re
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=".env")

from clients.azure_openai import AzureOpenAIClient
from tools.main import calculate, wikipedia
# from clients.ollama import OllamaClient

system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

Example session:
Question: What is the capital of China?
Thought: I should look up China on Wikipedia.
Action: wikipedia: China
PAUSE

You will be called again with this:

Observation: China is a country. The capital is Beijing.

You then output:

Answer: The capital of China is Beijing.
""".strip()


base_client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = ""
)
eval_client = AzureOpenAIClient(
        api_key = os.getenv("azure_openai_key"), 
        endpoint = "ssayjc.openai.azure.com",
        deployment_name="ssayjc-gpt-4o",
        api_version="2024-08-01-preview",
        system_prompt=""
)

def run_reflection(client, eval_client, question, n_iter=10):
    eval_client.system_prompt = f"""Evaluate how good the following response is, given the question. If the response ise poor, respond with your evaluation on what to improve with the response.
    If the response is good and does not need changes, append the following to the end of your response: <OK>. 
    Question: {question}.
    Response: """
    step = 0
    while step < n_iter:
        step+=1
        response = client.generate_completion(question)
        print(f"Responder: My initial response is: {response}")
        print(f"Responder: I will send this to the evaluator")
        ## Save to client memory
        evaluation_of_response = eval_client.generate_completion(response)
        print(f"Evaluator: My evaluation is {evaluation_of_response}")
        ## Save to evaluation memory
        if "<OK>" in evaluation_of_response:
            print("Stop reflection loop.")
            break
        else: 
            question = response
    return response


run_reflection(base_client, eval_client, "Other than knock knock jokes, what else did I ask related to Camille?")

