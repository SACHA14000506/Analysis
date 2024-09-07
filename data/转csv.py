import pickle
import pandas as pd 

pkl_file_path = './deepjit/features_test.pkl'  
with open(pkl_file_path, 'rb') as file:
    data = pickle.load(file)

print("数据类型:", type(data))

print("数据的前几个元素:")
for i, item in enumerate(data[:5]): 
    print(f"元素 {i+1}: {type(item)}，内容: {item}")

if isinstance(data, list):
    
    try:
        df = pd.DataFrame(data)
        print("成功转换为 DataFrame")
    except Exception as e:
        print("转换为 DataFrame 时出错:", e)
else:
    print("无法处理的数据类型:", type(data))

if 'df' in locals() and not df.empty:
    csv_file_path = './deepjit/features_test.csv' 
    df.to_csv(csv_file_path, index=False)
    print(f"数据已保存为 {csv_file_path}")
else:
    print("DataFrame 为空或未定义，未保存为 CSV 文件")