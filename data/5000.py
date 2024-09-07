import pandas as pd

input_file = 'data/paddle_data(20000).csv'
# df = pd.read_csv(input_file)
df = pd.read_csv(input_file, low_memory=False)
test_size = 2000
train_size = 3000

# 提取前5000行作为测试集
test_df = df.head(test_size)
test_df.to_csv('data/paddle_test.csv', index=False)

# 提取之后15000行作为训练集
train_df = df.iloc[test_size:test_size + train_size]
train_df.to_csv('data/paddle_train.csv', index=False)

print("CSV文件已成功分割为 test.csv 和 train.csv")
