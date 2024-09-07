import pandas as pd

def rename_columns(df):

    if 'bug' in df.columns:
        df.rename(columns={'bug': 'is_buggy_commit'}, inplace=True)

mxnet_df = pd.read_csv('commit_new2.csv')
features_df = pd.read_csv('expanded_file.csv')
# features_df = pd.read_csv('data/features_train.csv')

rename_columns(features_df)

unique_features_cols = set(features_df.columns) - set(mxnet_df.columns)
features_df.drop(columns=unique_features_cols, inplace=True, errors='ignore')

min_length = min(len(mxnet_df), len(features_df))
features_df = features_df.iloc[:min_length]

common_columns = set(features_df.columns) & set(mxnet_df.columns)

# 只替换共有的列
for col in common_columns:
    features_df[col] = mxnet_df[col]

output_path = 'data/commit_new_test.csv'
features_df.to_csv(output_path, index=False)

print(f'Data has been written to {output_path}')