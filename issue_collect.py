import requests
import pandas as pd
from dateutil.parser import parse
import pytz  
import time


# 性能相关的关键词
KEYWORDS = [
    "performance regression", "regression in performance", "degradation", "laggy",
    "decline in performance", "lower performance", "worse performance", "worsening performance",
    "bad performance", "deterioration", "performance bug", "poor performance", "latency",
    "slowdown", "slower", "slow", "throughput", "hit in performance", "performance hit",
    "drop in performance", "performance drop", "worsen performance", "worsened performance",
    "memory leak", "memory issue", "memory usage", "gpu usage", "cpu usage", "response time"
]


def get_issue_labels(issue_url):
    response = requests.get(issue_url, headers=HEADERS)
    if response.status_code == 200:
        issue_data = response.json()
        return [label['name'] for label in issue_data.get('labels', [])]
    return []


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

#2000tiao
def search_performance_issues(repo_owner, repo_name, start_date='2022-01-01', end_date='2023-12-31', limit=2000):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    params = {
        'since': start_date + 'T00:00:00Z',
        'until': end_date + 'T23:59:59Z',
        'per_page': 100,
        'state': 'closed'  # 关闭的issue
    }

    issues_data = []
    page = 1

    utc = pytz.utc

    try:
        while len(issues_data) < limit:
            response = requests.get(url, headers=HEADERS, params={**params, 'page': page})
            if response.status_code != 200:
                print(f"Error fetching issues: {response.status_code}")
                break

            issues = response.json()
            if not issues:
                break

            for issue in issues:
                if 'pull_request' in issue:
                    continue

                issue_body = issue.get('body', '').lower()
                issue_date = parse(issue['created_at']).astimezone(utc)

                if any(keyword in issue_body for keyword in KEYWORDS):
                    issue_labels = get_issue_labels(issue['url'])
                    issues_data.append({
                        'issue_number': issue['number'],
                        'title': issue['title'],
                        'author': issue['user']['login'],
                        'created_at': issue_date,
                        'body': issue_body,
                        'issue_labels': ', '.join(issue_labels) 
                    })

                    # 打印条数
                    print(f"已找到信息条数: {len(issues_data)}")

                if len(issues_data) >= limit:
                    break

            page += 1
            time.sleep(1)  # 添加请求间隔

    except KeyboardInterrupt:
        print("程序中断，保存已有数据")
        save_to_csv(issues_data, '/home/cass/Webstorm_project/MSR2024-Replication-Package/output/tensor.csv')

    save_to_csv(issues_data, '/home/cass/Webstorm_project/MSR2024-Replication-Package/output/tensor.csv')
    print("结果已保存到 tensor.csv")

repo_owner = 'tensorflow'
repo_name = 'tensorflow'
search_performance_issues(repo_owner, repo_name)
