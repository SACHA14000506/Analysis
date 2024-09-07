import pandas as pd

csv_file_path = 'data/features_test.csv' 
df = pd.read_csv(csv_file_path)


pkl_file_path = 'data/features_test.pkl' 
df.to_pickle(pkl_file_path)
