from github import Github
import os
from pprint import pprint

user_name = 'EnvironmentalSystems'
repositories = ['ClearWater', 'ProjectManagement']
token = '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'
state = 'open'

# token = os.getenv('GITHUB_TOKEN', '...')
g = Github(token)

for repo_name in repositories:
    full_repo_name = '{}/{}'.format(user_name, repo_name)
    print()
    print('Issues in repository: {}'.format(full_repo_name))
    repo = g.get_repo(full_repo_name)
    issues = repo.get_issues(state=state)
    # pprint(issues.get_page(0))
    for issue in issues:
        print('#: {}, title: {}' .format(issue.number, issue.title))
