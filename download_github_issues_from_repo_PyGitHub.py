'''
Download "Issues" from GitHub

This version uses the "PyGitHub" module, which provides a relatively 
limited amount of information, but it is easy to use.

This script was created using information provided by:
https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131

Author: Todd Steissberg
Date: June 6, 2021
'''

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
    full_repo_name = f'{user_name}/{repo_name}'
    print(f'\nIssues in repository: {full_repo_name}')
    repo = g.get_repo(full_repo_name)
    issues = repo.get_issues(state=state)
    # pprint(issues.get_page(0))
    for issue in issues:
        print('#: {}, title: {}' .format(issue.number, issue.title))