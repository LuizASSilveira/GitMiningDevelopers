import json
import arrow
from src.gitHubApiRequest import performRequest

path = 'C:\\Users\\luiz_\\Desktop\\data\\rafaelfranca\\userCommit.json'
file = open(path, 'r')
dev = json.load(file)
file.close()

devCommiter = {}


def getLanguageFile(commits):
    commits = commits.splitlines()
    extentions = []
    for line in commits:
        if 'diff' in line[:4]:
            extentions.append(line.split('/')[-1].split('.')[-1])
    return extentions


for d in dev:
    dateCommit = arrow.get(d['committedDate']).format('YYYY/MM')
    print(d['url'] + '.diff')
    commitFile = performRequest(d['url'] + '.diff').text
    print(getLanguageFile(commitFile))

    # if not (dateCommit in devCommiter.keys()):
    #     devCommiter[dateCommit] = [dateCommit]


