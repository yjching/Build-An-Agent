#### Current Progress
---


What works:
* Asking the LLM to generate a SQL query and execute it. You must give the input table to reference (can be JSON) and it will return the result (this example using DuckDB).

What kind of works:
* Using ReAcT with the below prompt.
* The first loop, the LLM will execute the get_table_from_db and bring back a JSON of the correct input.
* The second loop, the LLM will use the output from the first loop to come up with the correct SQL query to execute. ** It will then hallucinate an Observation and even hallucinate the Answer **. This hallucination is correct most of the time (!) but not 100%.
* The correct tool will not execute though.
```python
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
```