def get_table_from_db(table_name, db_con):
    return db_con.sql(f"SELECT * FROM {table_name};").to_df().to_json()

def execute_sql_query(sql_query, db_con):
    return db_con.sql(f"{sql_query}").to_df().to_json()