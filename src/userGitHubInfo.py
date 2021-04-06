from src.gitHubApiRequest import requestApiGitHubV4, performRequest
from src.fileAnalyze import userCommitModification
from datetime import date
import pandas as pd


def getContributors(size=50):
    resp = performRequest('https://api.github.com/repos/rails/rails/contributors?per_page={}&order=desc'.format(size)).json()
    return [urlUser['login'] for urlUser in resp][:size]


def getQueryFile(nameQuery):
    file = open('./querys/{}.graphql'.format(nameQuery), 'r')
    gitHubQuery = file.read()
    file.close()
    return gitHubQuery


def getUserInfo(usuerName):
    query = getQueryFile('userInformation')
    queryVariables = {'nameUser': usuerName}
    return requestApiGitHubV4(query, queryVariables)


def getUserInfByYear(loginUser, dateCreated):
    dateCreated = dateCreated.split("-")
    yearCreated = int(dateCreated[0])
    monthCreated = int(dateCreated[1])
    flagMonth = True

    todayDate = str(date.today()).split('-')
    todayYear = int(todayDate[0])
    todayMonth = int(todayDate[1])
    userYearInfo = {}

    while yearCreated <= todayYear:

        yearCreated = yearCreated

        if flagMonth:
            month = monthCreated
            flagMonth = False
        else:
            month = 1
        userMonthInfo = {}

        while True:
            if month > 12 or (yearCreated == todayYear and month > todayMonth):
                break

            monthAux = str(month)
            monthAux = (str(0) + monthAux) if month < 10 else monthAux
            queryVariables = {
                "nameUser": loginUser,
                "fromDate": '{}-{}-01T04:00:00Z'.format(yearCreated, monthAux),
                "toDate": '{}-{}-31T23:59:59Z'.format(yearCreated, monthAux),
            }
            query = getQueryFile('userInfoContributionsCollection')
            userMonthInfo[month] = requestApiGitHubV4(query, queryVariables)['data']['user']["contributionsCollection"]
            print('{}/{}: {}'.format(yearCreated, month, list(userMonthInfo[month].values())))
            userYearInfo['{}/{}'.format(yearCreated, month)] = list(userMonthInfo[month].values())
            keys = userMonthInfo[month].keys()
            month += 1

        yearCreated += 1
        # if yearCreated == 2010:
        #     break
    return userYearInfo, keys


def repositoryUser(loginUser, numPage=80):
    queryVariables = {
        "nameUser": loginUser,
        "numPage": numPage
    }
    # repositoryAffiliation = {'OWNER': [], 'COLLABORATOR': [], 'ORGANIZATION_MEMBER': []}
    repositoryAffiliation = {'OWNER': [], 'COLLABORATOR': []}
    for repAff in repositoryAffiliation.keys():
        # print("\n")
        queryVariables["RepositoryAffiliation"] = repAff
        query = getQueryFile('repositoryInfo')
        while True:
            resp = requestApiGitHubV4(query, queryVariables)
            for rep in resp['data']['user']['repositories']['nodes']:
                # print(repAff + '---> ' + rep["nameWithOwner"])
                repositoryAffiliation[repAff].append(rep)
            if not resp['data']['user']['repositories']['pageInfo']['hasNextPage']:
                break
            query = getQueryFile('repositoryInfNext')
            queryVariables["after"] = resp['data']['user']['repositories']['pageInfo']['endCursor']
    # return repositoryAffiliation['OWNER'], repositoryAffiliation['COLLABORATOR'], repositoryAffiliation['ORGANIZATION_MEMBER']
    return repositoryAffiliation['OWNER'], repositoryAffiliation['COLLABORATOR']


def getUserRepositoryCommit(userID, arrayRepository, numPage=100):
    arrayCommits = []
    for repository in arrayRepository:
        print(repository['nameWithOwner'])
        owner, name = repository['nameWithOwner'].split('/')
        if name == "linux":
            'Ignorou repositorio linux por nao retornar o historico via api'
            continue

        queryVariables = {
            "numPageIssues": numPage,
            "idUser": userID,
            "owner": owner,
            "name": name
        }
        query = getQueryFile('userRepositoryCommit')

        while True:
            resp = requestApiGitHubV4(query, queryVariables)
            # print(resp)
            if not resp['data']['repository']['defaultBranchRef']:
                break

            resp = resp['data']['repository']['defaultBranchRef']['target']['history']
            for number, commit in enumerate(resp['nodes']):
                # print(number, commit['url'])
                arrayCommits.append(commit)

            if not resp['pageInfo']['hasNextPage']:
                break

            query = getQueryFile('userRepositoryCommitNext')
            queryVariables["after"] = resp['pageInfo']['endCursor']
    return arrayCommits


def userCommitDiffInfo(userCommits):
    addicted = list()
    deletions = list()
    invalidCommit = {}
    for commitLink in userCommits:

        print(commitLink['url'])
        response = performRequest(commitLink['url'] + '.diff')
        if response.status_code != 200:
            print('---->', commitLink['url'])
            print('---->', response.status_code)
            if invalidCommit.get(response.status_code):
                invalidCommit[response.status_code].append(response.text)
            else:
                invalidCommit[response.status_code] = [response.text]
            continue

        add, remove = userCommitModification(response.text)
        addicted.extend(add)
        deletions.extend(remove)
        print('-->', len(add))
        print('-->', len(remove))

    print('addicted -->', len(addicted))
    print('deletions -->', len(deletions))
    print('invalidCommit -->', len(invalidCommit))
    print('invalidCommit -->', invalidCommit)
    print('invalidCommit -->', invalidCommit.keys())
