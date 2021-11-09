import json
from pprint import pprint

import arrow
from src.gitHubApiRequest import performRequest

path = 'C:\\Users\\luiz\\Desktop\\userCommit.json'
file = open(path, 'r')
commits = json.load(file)
file.close()

devCommiter = {}


def getLanguageFile(commits):
    commits = commits.splitlines()
    extentions = []
    for line in commits:
        if 'diff' in line[:4]:
            extentions.append(line.split('/')[-1].split('.')[-1])
    return extentions

devFiles = {}
for commit in commits:
    dateCommit = arrow.get(commit['committedDate']).format('YYYY/MM')
    idCommit = commit['url'].split('/')[-1]

    print(commit['url'] + '.diff')
    commitFile = performRequest(commit['url'] + '.diff').text

    if dateCommit in devFiles.keys():
        devFiles[dateCommit].append({idCommit: getLanguageFile(commitFile)})
    else:
        devFiles[dateCommit] = [{idCommit: getLanguageFile(commitFile)}]

pprint(devFiles)


