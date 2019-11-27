import pandas as pd

s = pd.read_sql_table((101, 1001, 'caoweijun', 'Security Department', datetime.date(2003, 5, 16), datetime.date(2025, 12, 20)),
        (102, 1002, 'caoyajun', 'Security Department', datetime.date(2002, 6, 7), datetime.date(2024, 11, 16)),
        (103, 1003, 'caoyi', 'Security Department', datetime.date(2002, 3, 23), datetime.date(2026, 9, 27)))

df = pd.read_csv('./sql/contracts.csv', dtype=[])
df['start_date'] = pd.to_datetime(df['start_date'])
# df['start_date'].min()
l1 = pd.date_range(start=df['start_date'].min(), end=df['start_date'].max(), freq='3M')
# df['start_date'].dt.month
l2 = list(df['start_date'].groupby(df.start_date.dt.to_period("3M")).agg('count').values.astype(int))
df

