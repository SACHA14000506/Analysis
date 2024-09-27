import json
import os
import sys
from github import Github
from dotenv import load_dotenv

# 加载 GitHub Token
load_dotenv('token.env')
token = os.getenv('GITHUB_TOKEN')

if token is None:
    print("GITHUB_TOKEN is not set in the environment", file=sys.stderr)
    raise SystemExit(1)

def read_keywords(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def format_date(date):
    if date is None:
        return None
    return date.isoformat()

def find_all_bugs(github_client, owner, repo, keywords):
    repo = github_client.get_repo(f"{owner}/{repo}")
    issues = []
    closed_issues = repo.get_issues(state='closed')

    for issue in closed_issues:
        for keyword in keywords:
            if keyword in issue.title or keyword in (label.name for label in issue.labels):
                issues.append({
                    "key": f"{repo.name}-{issue.number}",
                    "fields": {
                        "created": format_date(issue.created_at),
                        "resolutiondate": format_date(issue.closed_at)
                    }
                })
                print(f"找到已关闭问题: {issue.title}，关键字: {keyword}")
                break  

    print(f"找到 {len(issues)} 个已关闭的问题。")
    return issues

def main(owner, repo):
    keywords = read_keywords('./key.csv') 
    github_client = Github(token)
    issues = find_all_bugs(github_client, owner, repo, keywords)  
    result = {
        "expand": "schema, names",
        "startAt": 0,
        "maxResults": len(issues),
        "total": len(issues),
        "issues": issues
    }


    if not os.path.exists("fetch_issues"):
        os.makedirs("fetch_issues")

    with open("fetch_issues/res0.json", 'w') as output_file:
        json.dump(result, output_file, indent=4)


if len(sys.argv) < 3:
    print("用法: python fetch_github.py <owner> <repo>")
    sys.exit(1)

if __name__ == "__main__":
    owner = sys.argv[1]
    repo = sys.argv[2]
    main(owner, repo)

