import os

from src.gitHubApiRequest import performRequest
from pprint import pprint
from os import listdir
import pandas as pd
import json
import arrow


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


def devLanguagem(devColetede, devProjWithUser):
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

    return devlanguage, devRep


def organizesLanguageAndProjects(devColetede, devProjWithUser):

    devlanguage, devRep = devLanguagem(devColetede, devProjWithUser)
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


def listar_arquivos(caminho=None):
    lista_arqs = [arq for arq in listdir(caminho)]
    return lista_arqs


def getLanguageFile(commits):
    extentions = []
    for line in commits:
        if 'diff' in line[:4]:
            extentions.append(line.split('/')[-1].split('.')[-1])
    return extentions


# def fileExtencion(url, devColetede):
#     arquivos = listar_arquivos(url + '\\devs')
#     devFiles = {}
#
#     for dev in devColetede['login'][:2]:
#         if not dev in arquivos:
#             print(dev)
#             continue
#         try:
#
#             path = url + '\\devs\\' + dev + '\\userCommit.json'
#             file = open(path, 'r')
#             commits = json.load(file)
#             file.close()
#
#             devFiles[dev] = {}
#
#             for commit in commits:
#                 dateCommit = arrow.get(commit['committedDate']).format('YYYY/MM')
#                 idCommit = commit['url'].split('/')[-1]
#
#                 # print(commit['url'] + '.diff')
#                 commitFile = performRequest(commit['url'] + '.diff').text
#
#                 if dateCommit in devFiles.keys():
#                     devFiles[dev][dateCommit].append({idCommit: getLanguageFile(commitFile)})
#                 else:
#                     devFiles[dev][dateCommit] = [{idCommit: getLanguageFile(commitFile)}]
#
#             a_file = open(url+"\\devsExtencion.json", "w")
#             json.dump(devFiles, a_file)
#             a_file.close()
#
#         except:
#             print('Error ---> ', dev)
#             continue


def colleteCommits(url, devColetede, dev750):
    arquivos = listar_arquivos(url + '\\devs')
    # print(list(devColetede['login']).index('bripkens'))

    for index, dev in enumerate(dev750[250:]):
        print(index, ' ->', dev)
        filePath = url + '\\devs\\' + dev + "\\devsExtencion.json"

        if (not dev in arquivos):
            print('PULOU ->', dev)
            continue

        try:
            path = url + '\\devs\\' + dev + '\\userCommit.json'
            file = open(path, 'r')
            commits = json.load(file)
            file.close()

            devFiles = {}
            print(len(commits))
            for ind, commit in enumerate(commits):

                dateCommit = arrow.get(commit['committedDate']).format('YYYY/MM')
                idCommit = commit['url'].split('/')[-1]
                if ind % 100 == 0:
                    print(ind, '-> ', commit['url'] + '.diff')

                commitFile = performRequest(commit['url'] + '.diff').text
                commitFile = commitFile.splitlines()

                if commitFile.__len__() < 3:
                    continue

                if dateCommit in devFiles.keys():
                    devFiles[dateCommit].append({idCommit: commitFile})
                else:
                    devFiles[dateCommit] = [{idCommit: commitFile}]

            a_file = open(filePath, "w")
            json.dump(devFiles, a_file)
            a_file.close()

        except:
            print('Error ---> ', dev)
            continue


def dev750(devColetede, devProjWithUser):

    first250 = {
        'JavaScript': [],
        'c': [],
        'Ruby': [],

    }
    devlanguage, devRep = devLanguagem(devColetede, devProjWithUser)
    devColetSort = devColetede.sort_values(['totalCommitContributions'], ascending=False)

    for index, dev in devColetSort.iterrows():

        if first250['JavaScript'].__len__() < 250 and 'JavaScript' in devlanguage[dev['login']]:
            first250['JavaScript'].append(dev['login'])

        if first250['c'].__len__() < 250 and 'c' in devlanguage[dev['login']]:
            first250['c'].append(dev['login'])

        if first250['Ruby'].__len__() < 250 and 'Ruby' in devlanguage[dev['login']]:
            first250['Ruby'].append(dev['login'])

    a_file = open('C:\\Users\\luiz\\Desktop\\Teste.json', "w")
    json.dump(first250['JavaScript'] + first250['c'] + first250['Ruby'], a_file)
    a_file.close()


def processCommit(devs, url):
    for dev in devs:
        fileCommit = url + '\\devs\\' + dev + "\\devsExtencion.json"
        fileDevLanguages = url + '\\devs\\' + dev + "\\devslanguages.json"
        if (not os.path.isfile(fileCommit)) or os.path.isfile(fileDevLanguages):
            continue

        dateCommits = json.load(open(fileCommit, 'r'))
        devFiles = {}
        print(dev)
        for date in dateCommits.keys():
            for commits in dateCommits[date]:
                for commitId in commits.keys():
                    if date in devFiles.keys():
                        devFiles[date].append({commitId: getLanguageFile(commits[commitId])})
                    else:
                        devFiles[date] = [{commitId: getLanguageFile(commits[commitId])}]

        a_file = open(url + '\\devs\\' + dev + '\\devslanguages.json', "w")
        json.dump(devFiles, a_file)
        a_file.close()


def processLanguagem(devList, url):

    languagesExtentions = {
        # 'all': ['cpp', 'cxx', 'c', 'h', 'java', 'hh', 'hpp', 'h++', 'hxx', 'js', 'jsx', 'c', 'h', 'cs', 'py', 'go', 'php', 'kt', 'kts', 'rs', 'rlib', 'dart', 'rb', 'readme'],
        'JavaScript': ['js', 'jsx'],
        'Java': ['java'],
        'C++': ['cpp', 'cxx', 'c', 'C', 'h', 'hh', 'hpp', 'h++', 'hxx'],
        'C': ['c', 'h'],
        'C#': ['cs'],
        'Python': ['py'],
        'Go': ['go'],
        'PHP': ['php'],
        'Kotlin': ['kt', 'kts'],
        'Rust': ['rs', 'rlib'],
        'Dart': ['dart'],
        'Ruby': ['rb']
    }

    for dev in devList:
        fileDevLanguages = url + 'devs\\' + dev + "\\devslanguages.json"
        if not os.path.isfile(fileDevLanguages):
            continue

        devCommit = json.load(open(fileDevLanguages, 'r'))
        extByDate = {}
        for date in devCommit.keys():
            languagesOccurrences = {
                'JavaScript': 0,
                'Java': 0,
                 'C++': 0,
                'C': 0,
                'C#': 0,
                'Python': 0,
                'Go': 0,
                'PHP': 0,
                'Kotlin': 0,
                'Rust': 0,
                'Dart': 0,
                'Ruby': 0
            }
            for commits in devCommit[date]:
                for commit in commits.keys():
                    for lang in languagesExtentions.keys():
                        for ext in languagesExtentions[lang]:
                            languagesOccurrences[lang] += commits[commit].count(ext)
            extByDate[date] = languagesOccurrences

        a_file = open(url + '\\devs\\' + dev + '\\extByMonth.json', "w")
        json.dump(extByDate, a_file)
        a_file.close()


def generateDevsByLanguage(devList, url):
    listDevsExt = {}
    for dev in devList:
        fileDevExtentions = url + 'devs\\' + dev + "\\extByMonth.json"
        if not os.path.isfile(fileDevExtentions):
            continue

        devExtentions = json.load(open(fileDevExtentions, 'r'))
        languagesOccurrences = {
                'JavaScript': 0,
                'Java': 0,
                 'C++': 0,
                'C': 0,
                'C#': 0,
                'Python': 0,
                'Go': 0,
                'PHP': 0,
                'Kotlin': 0,
                'Rust': 0,
                'Dart': 0,
                'Ruby': 0
            }

        for date in devExtentions.keys():
            for lang in languagesOccurrences.keys():
                languagesOccurrences[lang] += devExtentions[date][lang]

        listDevsExt[dev] = languagesOccurrences

    df = pd.DataFrame(data=listDevsExt)
    dfT = df.T
    dfT.to_csv('C:\\Users\\luiz_\\OneDrive\\Área de Trabalho\\saida.csv')


if __name__ == '__main__':
    url = 'C:\\Users\\luiz_\\OneDrive\\Área de Trabalho\\gitMiningDevelopers\\src\\data\\'
    devColetede = pd.read_csv(url + "full.csv")
    devProjWithUser = json.load(open(url + 'ProjWithUser.json', 'r'))
    devList = json.load(open(url + 'devs.json', 'r'))
    dev750 = json.load(open('C:\\Users\\luiz_\\OneDrive\\Área de Trabalho\\dev750.json', 'r'))


    # devNotColetede(devColetede, devList)
    # organizesLanguageAndProjects(devColetede, devProjWithUser)
    # origin(devColetede)

    colleteCommits(url, devColetede, dev750)
    # processCommit(dev750, url)
    # processLanguagem(dev750, url)
    # generateDevsByLanguage(dev750, url)