import re
import json
import math
from typing import Callable
from clients.ollama import OllamaClient
from prompts.base_prompts import ORIGINAL_REACT_SYSTEM_PROMPT, REACT_SYSTEM_PROMPT
from tools.base_tools import get_space_news
from strategies.react import ReActStrategy

## ReAcT
base_client = OllamaClient(
    model_name="mistral",
    system_prompt="Your role is to translate the question into a SQL query to run on a dataset."
)

base_client.generate_completion("How many customers bought a product last year?")

agent = ReActStrategy(base_client, [get_space_news])


sql_question = "Find the ids of products that are both low fat and recyclable."

import duckdb
duckdb.sql("SELECT 42").show()

import pandas as pd

data = {
    'product_id': [0, 1, 2, 3, 4],
    'low_fats': ['Y', 'Y', 'N', 'Y', 'N'],
    'recyclable': ['N', 'Y', 'Y', 'Y', 'N']
}
df = pd.DataFrame(data)

con = duckdb.connect(r"D:\Build-An-Agent\database\file.db")
df.to_sql("Products", con, index=False)

con.sql("SELECT * FROM Products;").write_parquet(r"D:\Build-An-Agent\database\products.parquet")

con.sql("""
SELECT product_id
FROM Products
WHERE low_fats = 'Y' and recyclable = 'Y';
""")

input_table_as_json = con.sql("SELECT * FROM Products;").to_df().to_json()
input_table_as_json

system_prompt = f"""You are an expert in SQL. Your task is to translate the question into a SQL query, which references the provided table. Your output must only contain the SQL query.

Table: {input_table_as_json}"""

base_client = OllamaClient(
    model_name="mistral",
    system_prompt=system_prompt
)

base_client.generate_completion(sql_question)

base_client.generate_completion("What is this table for?")
base_client.generate_completion("Is product_id 1 low-fat and recyclable?")

## TODO
## * LLM can generate SQL query. Next step is to execute this query and then return the result. The result is a table, which goes back to the LLM to return the answer.
## * Need to create the initial load, which I've done as JSON manually now. This is the first loop - get the data to the LLM after question is asked.
## * Need to create another loop (the 3rd) where the result table returns to the LLM which translates it into an english output.