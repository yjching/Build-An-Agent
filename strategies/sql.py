from strategies.base_strategy import BaseStrategy
import duckdb


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
