from strategies.base_strategy import BaseStrategy
from strategies.react import ReActStrategy
from tools.sql_tools import get_table_from_db, execute_sql_query
import re

sql_tool_list = {
    "get_table_from_db": get_table_from_db,
    "execute_sql_query": execute_sql_query
}


class SQLExecutor(BaseStrategy):
    def __init__(self, base_client, db_connection):
        super().__init__(base_client)
        self.db_connection = db_connection
    def run(self, question):
        sql_query = self.base_client.generate_completion(question)
        print(sql_query)
        return self.db_connection.sql(f"{sql_query}")

class SQLAsker(BaseStrategy):
    '''When you want your output in plain English.'''
    def __init__(self, base_client, db_connection):
        super().__init__(base_client)
        self.db_connection = db_connection
    def run(self, question):
        prompt_to_reset = self.base_client.system_prompt
        sql_query = self.base_client.generate_completion(question)
        output_table = self.db_connection.sql(f"{sql_query}").to_df().to_json()
        responder_client_system_prompt = f"""You are given a table that answers the original input question. Ignore the table index as a source of information, just read the column values.
        Table: {output_table}
        Question: 
        """
        self.base_client.system_prompt = responder_client_system_prompt
        output_response = self.base_client.generate_completion(question)
        self.base_client.system_prompt = prompt_to_reset
        return output_response
    
class SQLReactStrategy(ReActStrategy):
    def __init__(self, base_client, db_con, tools_list=sql_tool_list):
        super().__init__(base_client, tools_list)
        self.db_con = db_con
    def run(self, question, n_iter=3):
        next_prompt = question
        i = 0
        while i < n_iter:
            i += 1
            result = self.base_client.generate_completion(next_prompt)
            print(result)
            if "PAUSE" in result and "Action" in result:
                action = re.findall(r"Action: ([a-z_]+): (.+)", result, re.IGNORECASE)
                print(action)
                tool_to_run = action[0][0]
                argument_for_tool = action[0][1].replace(" PAUSE","")
                print("The action is ", action)
                tool_result = self.tools_list[tool_to_run](argument_for_tool, self.db_con)
                print("Tool result: ", tool_result)
                next_prompt = f"Observation: {tool_result}"



