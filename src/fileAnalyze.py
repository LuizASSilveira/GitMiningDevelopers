import json


def userCommitModification(commits):
    addicted = list()
    deletions = list()
    commits = commits.splitlines()
    commits.pop(0) if len(commits) != 0 else commits

    for line in commits:
        if len(line) > 2 and line[0] == '+' and line[2] != '+':
            addicted.append(line[1:].strip())
        elif len(line) > 2 and line[0] == '-' and line[2] != '-':
            deletions.append(line[1:].strip())
    return addicted, deletions


def saveJson(data, dir, nameFile, typeOpen='w', encodingFile='UTF-8'):
    dirFull = dir + '\\' + nameFile
    file = open(dirFull, typeOpen, encoding=encodingFile)
    if data:
        json.dump(data, file, indent=4)
    file.close()
