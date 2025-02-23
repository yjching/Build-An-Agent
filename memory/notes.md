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

# Question: What is 4 * 5?
# Thought: I should calculate using the numbers provided. 
# Action: calculate: 4*5
# PAUSE

# You will be called again with this:

# Observation: 4 times 5 is 20.

# You then output:

# Answer: 20.



original_system_prompt = """
You are a function calling AI model. You operate by running a loop with the following steps: Thought, Action, Observation.

Use Thought to translate the question into a SQL query, on the provided input table. Your output must only contain the SQL query.
Use Action to run the SQL query, then return PAUSE.
Observation is the interpretation of the result of running the actions.

Example session:
Question: From the products table, find the ids of products that are both low fat and recyclable.
Thought: I need to convert the above question into a SQL query and run it on the specified input table.
Action: sql_execute: SELECT product_id FROM products WHERE low_fats = 'Y' AND recyclable = 'Y';
PAUSE

You will be called again with this:
Observation: '{"product_id":{"0":1,"1":3}}'
You then output:
Answer: The ids of products that are both low fat and recyclable are 1 and 3.
"""

system_prompt = original_system_prompt + f"\nTable: {input_table_as_json}"

pattern = r'sql_execute: (.*?);\nPAUSE'
match = re.search(pattern, output['message']['content'])
sql_query = match.group(1)
sql_query
