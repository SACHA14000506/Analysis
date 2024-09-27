import json


file_path = '/home/cass/Webstorm_project/SZZ_github/z3/results/fix_and_introducers_pairs.json'


with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 计算对的数量
pair_count = len(data)

print(f"共有 {pair_count} 对 ID。")

