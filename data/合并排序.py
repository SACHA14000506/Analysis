import pandas as pd

df1 = pd.read_csv('commit.csv')
df2 = pd.read_csv('commit_hun.csv')
df3 = pd.read_csv('commit_hun1.csv')

df = pd.concat([df1, df2, df3])

# 按照'author_date'排序
df_sorted = df.sort_values(by='author_date')

df_buggy = df_sorted[df_sorted['is_buggy_commit'] == 1]
df_non_buggy = df_sorted[df_sorted['is_buggy_commit'] == 0]

min_count = min(len(df_buggy), len(df_non_buggy))
df_buggy = df_buggy.head(min_count)
df_non_buggy = df_non_buggy.head(min_count)

df_balanced = pd.concat([df_buggy, df_non_buggy])

df_balanced_sorted = df_balanced.sort_values(by='author_date')

train_size = int(len(df_balanced_sorted) * 0.7)  # 70% 作为训练集
test_size = len(df_balanced_sorted) - train_size

train_df = pd.concat([
    df_buggy.head(int(train_size / 2)),
    df_non_buggy.head(int(train_size / 2))
])

test_df = pd.concat([
    df_buggy.tail(int(test_size / 2)),
    df_non_buggy.tail(int(test_size / 2))
])

train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)
