import pandas as pd

df = pd.read_csv('train.csv')

new_columns = [
    'project', 'parent_hashes', 'commit_hash', 'author_name', 'author_email',
    'author_date', 'author_date_unix_timestamp', 'commit_message', 'la', 'ld',
    'fileschanged', 'nf', 'ns', 'nd', 'entropy', 'ndev', 'lt', 'nuc', 'age',
    'exp', 'rexp', 'sexp', 'classification', 'fix', 'is_buggy_commit'
]

df.columns = new_columns

# 数据类型调整
df['author_date_unix_timestamp'] = pd.to_numeric(df['author_date_unix_timestamp'], errors='coerce').fillna(0).astype('int64')
df['la'] = pd.to_numeric(df['la'], errors='coerce').fillna(0).astype('int64')
df['ld'] = pd.to_numeric(df['ld'], errors='coerce').fillna(0).astype('int64')
df['nf'] = pd.to_numeric(df['nf'], errors='coerce').fillna(0).astype('int64')
df['ns'] = pd.to_numeric(df['ns'], errors='coerce').fillna(0).astype('int64')
df['nd'] = pd.to_numeric(df['nd'], errors='coerce').fillna(0).astype('int64')
df['entropy'] = pd.to_numeric(df['entropy'], errors='coerce').fillna(0.0).astype('float64')
df['ndev'] = pd.to_numeric(df['ndev'], errors='coerce').fillna(0).astype('int64')
df['lt'] = pd.to_numeric(df['lt'], errors='coerce').fillna(0.0).astype('float64')
df['nuc'] = pd.to_numeric(df['nuc'], errors='coerce').fillna(0).astype('int64')
df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0.0).astype('float64')
df['exp'] = pd.to_numeric(df['exp'], errors='coerce').fillna(0.0).astype('float64')
df['rexp'] = pd.to_numeric(df['rexp'], errors='coerce').fillna(0.0).astype('float64')
df['sexp'] = pd.to_numeric(df['sexp'], errors='coerce').fillna(0.0).astype('float64')
df['is_buggy_commit'] = pd.to_numeric(df['is_buggy_commit'], errors='coerce').fillna(0.0).astype('float64')

df['classification'] = df['classification'].fillna('Unknown')
df['fileschanged'] = df['fileschanged'].fillna('')
df['project'] = df['project'].fillna('')
df['parent_hashes'] = df['parent_hashes'].fillna('')
df['commit_hash'] = df['commit_hash'].fillna('')
df['author_name'] = df['author_name'].fillna('')
df['author_email'] = df['author_email'].fillna('')
df['author_date'] = df['author_date'].fillna('')
df['commit_message'] = df['commit_message'].fillna('')

df['fix'] = df['fix'].fillna(False).astype('bool')

df.to_csv('features_train.csv', index=False)

print("文件转换完成，已保存为2.csv")
