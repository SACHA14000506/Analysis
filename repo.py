


from github import Github

g = Github("")

repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')

if repositories.totalCount == 0:
    print("没有找到匹配的仓库。")
else:
    for repo in repositories[:10]:
        print(f"名称: {repo.name}, 星数: {repo.stargazers_count}, 更新时间: {repo.updated_at}")

