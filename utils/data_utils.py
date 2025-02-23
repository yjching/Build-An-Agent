import pandas as pd
import duckdb

def create_df_load_duckdb(table_name, input_dict: dict, con):
    df = pd.DataFrame(input_dict)
    df.to_sql(table_name, con, index=False)