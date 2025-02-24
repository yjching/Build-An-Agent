import os
import re
import json
import math
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=".env")

from clients.azure_openai import AzureOpenAIClient

from prompts.base_prompts import SQL_REACT_SYSTEM_PROMPT
from strategies.react import ReActStrategy

import duckdb
import pandas as pd

from utils.data_utils import create_df_load_duckdb

con = duckdb.connect(r"database/file.db")
## Load data
data = [
    {"id": 1, "name": "Will", "referee_id": None},
    {"id": 2, "name": "Jane", "referee_id": None},
    {"id": 3, "name": "Alex", "referee_id": 2},
    {"id": 4, "name": "Bill", "referee_id": None},
    {"id": 5, "name": "Zack", "referee_id": 1},
    {"id": 6, "name": "Mark", "referee_id": 2}
]
create_df_load_duckdb("Customer", data, con)

base_client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = SQL_REACT_SYSTEM_PROMPT
)
# sql_question = "From the products table, find the ids of products that are both low fat and recyclable."
tools = {
    "get_table_from_db": get_table_from_db,
    "execute_sql_query": execute_sql_query
}

def run(question):
    next_prompt = question
    i = 0
    while i < 3:
        i += 1
        result = base_client.generate_completion(next_prompt)
        print(i, result)
        if "PAUSE" in result and "Action" in result:
            action = re.findall(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
            print(action)
            tool_to_run = action[0][0]
            argument_for_tool = action[0][1].replace(" PAUSE","")
            print("The action is ", action)
            tool_result = tools[tool_to_run](argument_for_tool, con)
            print("Tool result: ", tool_result)
            next_prompt = f"Observation: {tool_result}"

run(question = "From the Customer table, find the names of the customers that were not referred by the customer with id 2, including customers who were not referred at all.")

run("From the Views table, find all authors that viewed at least one of their own articles.")


sql_question = "From the Customer table, find the names of the customers that were not referred by the customer with id 2, including customers who were not referred at all."
sql_query = "SELECT product_id FROM products WHERE low_fats = true AND recyclable = true"

sql_query = base_client.generate_completion(sql_question)
# sql_query = "SELECT product_id FROM products WHERE low_fats = 'Y' AND recyclable = 'Y'"

con.sql(f"SELECT product_id FROM products WHERE low_fats = true AND recyclable = true")
output_table = con.sql(f"{sql_query}").to_df().to_json()
output_table

base_client.generate_completion(output_table)


from strategies.sql import SQLAsker, SQLExecutor


system_prompt = F"""You are an expert in SQL. Your task is to translate the question into a SQL query, on the provided table. Your output must only contain the raw SQL query statement, without any other syntax.

Table: {input_table_as_json}
"""


agent = SQLExecutor(base_client, con)
agent.run("From the Customer table, find the names of the customers that were not referred by the customer with id 2, including customers who were not referred at all.")

## TODO
## * Need to create the initial load, which I've done as JSON manually now. This is the first loop - get the data to the LLM after question is asked.