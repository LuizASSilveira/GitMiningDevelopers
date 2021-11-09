from pprint import pprint

import pandas as pd
import json


def devNotColetede(dataframe, devList):
    print('Total: ', devList.__len__())
    print('Sem Repetidos: ', set(devList).__len__())
    print('Diferença: ', devList.__len__() - set(devList).__len__())
    print()

    ba = set(devList) - set(dataframe['login'])
    dataFrameSize = set(dataframe['login']).__len__()

    print('Database coletado: ', dataFrameSize)
    print('Removidos manual Bot: ', 10)
    print('QTD desenvolvedores não coletados: ', ba.__len__() - 10)


def organizesLanguageAndProjects(devColetede, devProjWithUser):
    devlanguage = {}
    devRep = {}

    for index, dev in devColetede.iterrows():
        devlanguage[dev['login']] = []
        devRep[dev['login']] = []
        for lang in devProjWithUser:
            for rep in devProjWithUser[lang]:
                for repName in rep:
                    for cont in rep[repName]:
                        if dev['login'] == cont['login']:
                            devlanguage[dev['login']].append(lang)
                            devRep[dev['login']].append(repName)

    countDvs = {
        'JavaScript': 0,
        'Ruby': 0,
        'c': 0
    }

    for dev in devlanguage:
        if 'JavaScript' in devlanguage[dev]:
            countDvs['JavaScript'] += 1

        if 'Ruby' in devlanguage[dev]:
            countDvs['Ruby'] += 1

        if 'c' in devlanguage[dev]:
            countDvs['c'] += 1

    print(countDvs)

    # desenvolvedores com mais de 1 linguagem e projetos
    countDevsMoreOnelanguage = 0
    countDevsMoreOneRep = 0
    maxLang = ['', 0]
    maxRep = ['', 0]

    for dev in devlanguage.keys():
        numlanguage = set(devlanguage[dev]).__len__()
        numRep = devlanguage[dev].__len__()

        if numlanguage > 1:
            countDevsMoreOnelanguage += 1

        if numRep > 1:
            countDevsMoreOneRep += 1

        if numlanguage > maxLang[1]:
            maxLang[0] = dev
            maxLang[1] = numlanguage

        if numRep > maxRep[1]:
            maxRep[0] = dev
            maxRep[1] = numRep

    print('Devs more One Language: ', countDevsMoreOnelanguage)
    print('Devs more One Repositorie: ', countDevsMoreOneRep)
    print('Maior numero de repositorios: ', maxRep)
    print('Maior numero de lang: ', maxLang)


def origin(df):
    totalColected = df['login'].__len__()
    origin = {
        'pullRequests': df.loc[df['pullRequests'] != 0].__len__(),
        'issues': df.loc[df['issues'] != 0].__len__(),
        'gists': df.loc[df['gists'] != 0].__len__(),
        'commitComments': df.loc[df['commitComments'] != 0].__len__(),
        'issueComments': df.loc[df['issueComments'] != 0].__len__(),
        'gistComments': df.loc[df['gistComments'] != 0].__len__(),
        'totalRepositoriesWithContributedPullRequestReviews': df.loc[df['totalRepositoriesWithContributedPullRequestReviews'] != 0].__len__(),

    }
    print(totalColected)

    print('pullRequests ', origin['pullRequests'], ',', (origin['pullRequests'] / totalColected) * 100)
    print('issues ', origin['issues'], ',', (origin['issues'] / totalColected) * 100)
    print('gists ', origin['gists'], ',', (origin['gists'] / totalColected) * 100)
    print('commitComments ', origin['commitComments'], ',', (origin['commitComments'] / totalColected) * 100)
    print('issueComments ', origin['issueComments'], ',', (origin['issueComments'] / totalColected) * 100)
    print('gistComments ', origin['gistComments'], ',', (origin['gistComments'] / totalColected) * 100)
    print('totalRepositoriesWithContributedPullRequestReviews ', origin['totalRepositoriesWithContributedPullRequestReviews'], ',', (origin['totalRepositoriesWithContributedPullRequestReviews'] / totalColected) * 100)


if __name__ == '__main__':
    devColetede = pd.read_csv("C:\\Users\\luiz_\\OneDrive\\Área de Trabalho\\full.csv")
    devProjWithUser = json.load(open('data/ProjWithUser.json', 'r'))
    devList = json.load(open('data/devs.json', 'r'))

    # devNotColetede(devColetede, devList)
    # organizesLanguageAndProjects(devColetede, devProjWithUser)
    origin(devColetede)




