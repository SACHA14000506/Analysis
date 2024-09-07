import pandas as pd

df = pd.read_csv('commit_hun.csv')

df_sorted = df.sort_values(by='author_date')

# 将前6000条记录保存到1.csv
df_sorted.head(100).to_csv('commit1.csv', index=False)

# 将后3000条记录保存到2.csv
df_sorted.tail(50).to_csv('commit2.csv', index=False)