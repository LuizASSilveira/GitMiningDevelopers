import sys
from src.gitHubApiV4Request import requestApiGitHubV4


def getToken():
    try:
        return sys.argv[1]
    except IndexError:
        print('Insira o tokem GitHub')
        exit(0)


def getQueryFile(nameQuery):
    file = open('./querys/{}.graphql'.format(nameQuery), 'r')
    gitHubQuery = file.read()
    file.close()
    return gitHubQuery


token = getToken()
query = getQueryFile('userInformation')
headers = {"Authorization": 'Bearer {0}'.format(token)}
variables = {'nameUser': 'LuizASSilveira'}

print(requestApiGitHubV4(query, headers, variables))
