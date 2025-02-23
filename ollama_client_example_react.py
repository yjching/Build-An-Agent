from os import system
import re
import json
import math
from typing import Callable
from clients.ollama import OllamaClient
from prompts.base_prompts import ORIGINAL_REACT_SYSTEM_PROMPT, REACT_SYSTEM_PROMPT
from tools.base_tools import get_space_news
from strategies.react import ReActStrategy

import duckdb
import pandas as pd

## ReAcT
base_client = OllamaClient(
    model_name="mistral",
    system_prompt="Your role is to translate the question into a SQL query to run on a dataset."
)


from utils.data_utils import create_df_load_duckdb

con = duckdb.connect(r"D:\Build-An-Agent\database\file.db")

def get_table_from_db(table_name, db_con):
    return db_con.sql(f"SELECT * FROM {table_name};").to_df().to_json()

def execute_sql_query(sql_query, db_con):
    return db_con.sql(f"{sql_query}").to_df().to_json()

system_prompt = """
You are a function calling AI model. You operate by running a loop with the following steps: Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.

Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:
get_table_from_db:
e.g. get_table_from_db: Sales
Return the given table from the database.

execute_sql_query:
e.g. execute_sql_query: SELECT cars FROM automobiles;
Execute the input SQL query.

Example session:

Question: From the products table, find the ids of products that are both low fat and recyclable.
Thought: I need to get the products table from the database.
Action: get_table_from_db: Products
PAUSE

You will be called again with this:
Observation: '{"product_id":{"0":0,"1":1,"2":2,"3":3,"4":4},"low_fats":{"0":"Y","1":"Y","2":"N","3":"Y","4":"N"},"recyclable":{"0":"N","1":"Y","2":"Y","3":"Y","4":"N"}}'

Thought: I need to create a SQL query on this table to find the ids of products that are both low fat and recyclable.
Action: execute_sql_query: SELECT product_id FROM products WHERE low_fats = true AND recyclable = true;
PAUSE

You will be called again with this:
Observation: '{"product_id":{"0":1,"1":3}}'

Answer: The ids of products that are both low fat and recyclable are 1 and 3.

Now it's your turn:
"""

# system_prompt = """
# You run in a loop of Thought, Action, PAUSE, Observation.
# At the end of the loop you output an Answer
# Use Thought to describe your thoughts about the question you have been asked.
# Use Action to run one of the actions available to you - then return PAUSE.
# Observation will be the result of running those actions.

# Your available actions are:
# execute_sql_query:
# e.g. execute_sql_query: SELECT cars FROM automobiles;
# Execute the input SQL query.

# Example session:

# Question: From the products table, find the ids of products that are both low fat and recyclable.
# Thought: I need to execute a SQL query on the products table to find the ids of products that are both low fat and recyclable.
# Action: execute_sql_query: SELECT product_id FROM products WHERE low_fats = true AND recyclable = true;
# PAUSE

# You will be called again with this:
# Observation: '{"product_id":{"0":1,"1":3}}'

# Answer: The ids of products that are both low fat and recyclable are 1 and 3.

# Now it's your turn on the following table. The name of the table will always be a single word between the words "From the" and "table".
# Table: """

# input_table_as_json = get_table_from_db("Customer", con)
# system_prompt+f"{input_table_as_json}"

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=system_prompt
)

# sql_question = "From the products table, find the ids of products that are both low fat and recyclable."
tools = {
    "get_table_from_db": get_table_from_db,
    "execute_sql_query": execute_sql_query
}

def run(question):
    next_prompt = question
    i = 0
    while i < 2:
        i += 1
        result = base_client.generate_completion(next_prompt)
        print(i, result)
        if "PAUSE" in result and "Action" in result:
            action = re.findall(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
            print("The action is ", action)
            tool_result = tools[action[0][0]](action[0][1], con)
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