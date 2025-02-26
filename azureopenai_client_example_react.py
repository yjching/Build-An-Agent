import os
import re
import json
import math
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=".env")

from clients.azure_openai import AzureOpenAIClient

from prompts.base_prompts import SQL_REACT_SYSTEM_PROMPT
from tools.sql_tools import get_table_from_db, execute_sql_query

from strategies.sql import SQLReactStrategy

import duckdb
import pandas as pd

from utils.data_utils import create_df_load_duckdb

con = duckdb.connect(r"database/file.db")

# Load data example 
# data = [
#     {"id": 1, "name": "Will", "referee_id": None},
#     {"id": 2, "name": "Jane", "referee_id": None},
#     {"id": 3, "name": "Alex", "referee_id": 2},
#     {"id": 4, "name": "Bill", "referee_id": None},
#     {"id": 5, "name": "Zack", "referee_id": 1},
#     {"id": 6, "name": "Mark", "referee_id": 2}
# ]

# create_df_load_duckdb("Customer", data, con)

base_client = AzureOpenAIClient(
    api_key = os.getenv("azure_openai_key"), 
    endpoint = "ssayjc.openai.azure.com",
    deployment_name="ssayjc-gpt-4o",
    api_version="2024-08-01-preview",
    system_prompt = SQL_REACT_SYSTEM_PROMPT
)

agent = SQLReactStrategy(base_client, con)

agent.run("From the Customer table, find the names of the customer that are not referred by the customer with id = 2.")
