'''
Download "Issues" from GitHub

This version uses the "requests" module, which provides access to much more information than provided by the
"PyGitHub" module.

This script was created using information provided by:
https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131

Author: Todd Steissberg
Date: June 6, 2021
'''

import requests
import os
from pprint import pprint


# Get data from GitHub
def get_request(user_name, repo_name, token, state='open'):
    query_url = f"https://api.github.com/repos/{user_name}/{repo_name}/issues?per_page=200"
    params = { 'state': state }
    headers = {'Authorization': f'token {token}'}
    issues = requests.get(query_url, headers=headers, params=params)
    return issues.json()

# Export results to CSV
def export_issues(outfile, user_name, repositories, token, state='open'):
    print(f'Processing: {repo_name}')
    issues = get_request(user_name, repo_name, token, state=state)
    print(f'Length of issues = {len(issues)}')
    g = open(outfile, 'w')
    g.write('Title,Labels\n')
    for issue in issues:
        try:
            title = issue['title']
            labels = issue['labels']
            hline = f'"{title}","'
            for label in labels:
                hline += label['name'] + ', '
            hline = hline.strip().strip(',') + '"\n'
            g.write(hline)
        except:
            print(issue)
    g.close
    # pprint(r.json())

# Export results to CSV, only if the specified label is in the issue
def export_issues_with_label(outfile, user_name, repositories, token, state='open', issue_label='bug'):
    print(f'Processing: {repo_name}')
    issues = get_request(user_name, repo_name, token, state='open')
    print(f'Length of issues = {len(issues)}')
    g = open(outfile, 'w')
    g.write('Title,Labels\n')
    for issue in issues:
        try:
            title = issue['title']
            labels = issue['labels']
            for label in labels:
                label_name = label['name']
                if label_name == issue_label:
                    g.write(f'"{title}","{label_name}"\n')
        except:
            print(issue)
    g.close

if __name__ == '__main__':
    user_name = 'EnvironmentalSystems'
    token = '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'

    repositories = [
        'ACTIONS',
        'ACT-ACF',
        'CE-QUAL-W2',
        'ClearWater',
        'Contracts',
        'Distribution',
        'EcoFutures',
        'General-Environmental-Water-Model',
        'Geospatial',
        'GitHub',
        'HEC-HMS-WQ',
        'HEC-RAS-WQ',
        'HEC-ResSim-WQ',
        'HEC-WAT-CE-QUAL-W2',
        'Ideas-and-Communication',
        'IDF',
        'MiddleEastModeling',
        'Papers',
        'ProjectManagement',
        'Proposals',
        'Ras2D_to_TecPlot',
        'SatelliteTools',
        'Satellite-HAB-Research',
        'ScreamingPlants',
        'Training',
        'WQ-Prototypes-and-Scripts'
    ]

    state = 'open'
    for repo_name in repositories:
        export_issues(f'output/{repo_name}_issues.csv', user_name, repositories, token, state=state)
        export_issues_with_label(f'output/{repo_name}_issues_with_bugs.csv', user_name, repositories, token, state=state, issue_label='effort: 8')