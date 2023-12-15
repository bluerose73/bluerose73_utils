import pandas as pd
from io import StringIO

def ParseTable(table: str, **kwargs):
    return ReadTable(StringIO(table), **kwargs)

def ReadTable(filename: str, **kwargs):
    df = pd.read_table(filename, sep = '|', header=0, skipinitialspace=True, **kwargs) \
             .dropna(axis=1, how='all').iloc[1:]
    df.columns = df.columns.str.strip()
    for column_name in df.columns:
        df[column_name] = df[column_name].str.rstrip(' %')
        try:
            df[column_name] = df[column_name].astype('float')
        except ValueError:
            pass

    return df