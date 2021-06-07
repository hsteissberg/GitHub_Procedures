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
def get_request(user_name, token, repo_name, params={}):
    query_url = f"https://api.github.com/repos/{user_name}/{repo_name}/issues?per_page=200"
    headers = {'Authorization': f'token {token}'}
    issues = requests.get(query_url, headers=headers, params=params)
    return issues.json()

# Export results to CSV
def export_issues(outfile, user_name, token, repositories, params={}, issue_labels=[]):
    print(f'Processing: {repo_name}')
    issues = get_request(user_name, token, repo_name, params=params)
    print(f'Number of issues: {len(issues)}')
    g = open(outfile, 'w')
    g.write('Title,Assignee,Labels\n')
    for issue in issues:
        try:
            title = issue['title']
            labels = issue['labels']
            assignees = issue['assignees']

            hline = f'"{title}",'

            if len(assignees) > 0:
                for assignee in assignees:
                    hline += f'''"{assignee['login']}", '''
                hline = hline.strip() # Save the trailing comma for creating the labels column
            else:
                hline += '"Not assigned",'
            
            # Optionally skip writing of the issue if the specified label is not found
            write_data = True
            if len(issue_labels) > 0:
                write_data = False

            # Iterate through labels and optionally check if a specified label is present
            if len(labels) > 0:
                for label in labels:
                    label_name = label['name']
                    if len(issue_labels) > 0:
                        if label_name in issue_labels:
                            write_data = True
                    hline += f'"{label_name}", '
                hline = hline.strip().strip(',') + '\n'
            else:
                hline += '"No labels"\n'

            if write_data:
                g.write(hline)
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

    # repositories = ['ScreamingPlants']

    for repo_name in repositories:
        params = { 'state': 'open'}
        export_issues(f'output/{repo_name}_open_issues.csv', user_name, token, repositories, params=params)
        params = { 'state': 'closed'}
        export_issues(f'output/{repo_name}_closed_issues.csv', user_name, token, repositories, params=params)
        params = { 'state': 'open'}
        export_issues(f'output/{repo_name}_issues_with_bugs.csv', user_name, token, repositories, params=params, issue_labels=['bug', 'effort: 8'])