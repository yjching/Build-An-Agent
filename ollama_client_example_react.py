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

data = {
    'product_id': [0, 1, 2, 3, 4],
    'low_fats': ['Y', 'Y', 'N', 'Y', 'N'],
    'recyclable': ['N', 'Y', 'Y', 'Y', 'N']
}
df = pd.DataFrame(data)

data2 = {
    'id': [1, 2, 3, 4, 5, 6],
    'name': ['Will', 'Jane', 'Alex', 'Bill', 'Zack', 'Mark'],
    'referee_id': [None, None, 2, None, 1, 2]
}
df2 = pd.DataFrame(data2)
df2.to_sql("Customer", con, index=False)


df.to_sql("Products", con, index=False)

con.sql("SELECT * FROM Products;").write_parquet(r"D:\Build-An-Agent\database\products.parquet")

# con.sql("""
# SELECT product_id
# FROM Products
# WHERE low_fats = 'Y' and recyclable = 'Y';
# """)

input_table_as_json = con.sql("SELECT * FROM Customer;").to_df().to_json()
input_table_as_json

# sql_question = "From the products table, find the ids of products that are both low fat and recyclable."
sql_question = "From the Customer table, find the names of the customers that were not referred by the customer with id 2, including customers who were not referred at all."
sql_query

# sql_query = base_client.generate_completion(sql_question)
# sql_query = "SELECT product_id FROM products WHERE low_fats = 'Y' AND recyclable = 'Y'"

con.sql(f"{sql_query}")
output_table = con.sql(f"{sql_query}").to_df().to_json()
output_table

base_client.generate_completion(output_table)

responder_client_system_prompt = f"""You are given a table that answers the original input question. Ignore the table index as a source of information, just read the column values.
Table: {output_table}
Question: 
"""

responder_client = OllamaClient(
    model_name="mistral",
    system_prompt=responder_client_system_prompt
)
responder_client.generate_completion(sql_question)

from strategies.sql import SQLAsker, SQLExecutor


system_prompt = F"""You are an expert in SQL. Your task is to translate the question into a SQL query, on the provided table. Your output must only contain the raw SQL query statement, without any other syntax.

Table: {input_table_as_json}
"""
con = duckdb.connect(r"D:\Build-An-Agent\database\file.db")

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=system_prompt
)

agent = SQLExecutor(base_client, con)
agent.run("From the Customer table, find the names of the customers that were not referred by the customer with id 2, including customers who were not referred at all.")

## TODO
## * Need to create the initial load, which I've done as JSON manually now. This is the first loop - get the data to the LLM after question is asked.