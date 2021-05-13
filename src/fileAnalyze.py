import json


def userCommitModification(commits):
    addicted = list()
    deletions = list()
    commits = commits.splitlines()
    print(commits)

    for line in commits:
        if len(line) > 2 and line[0] == '+' and line[2] != '+':
            addicted.append(line[1:].strip())
        elif len(line) > 2 and line[0] == '-' and line[2] != '-':
            deletions.append(line[1:].strip())
    return addicted, deletions


