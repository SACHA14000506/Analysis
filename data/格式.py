import pandas as pd

df = pd.read_pkl('features_test.pkl', nrows=5)  

#print(df.head())

print(df.info())