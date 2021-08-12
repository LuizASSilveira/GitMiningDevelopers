import json
import os
import sys

from src.gitHubApiRequest import performRequest
from src.utils import createFolderIfDoesntExist


def getContributors(path, language, numeroContribuidores=100, numeroProjetos=100, ignoreProjects=[]):
    listRepo = {}
    listDev = []

    for lang in language:
        url = 'https://api.github.com/search/repositories?q=language:{}+stars:">+1000"&sort={}&per_page={}&page=1&order=desc'.format(lang.lower(), 'stars', 100)
        print(url)
        print('\n')
        request = performRequest(url)
        listRepo[lang] = []
        numProjetByLanguage = numeroProjetos
        numberContributor = 0

        for proj in request.json()['items']:

            if numProjetByLanguage == 0:
                break

            if proj['full_name'] in ignoreProjects:
                continue

            numProjetByLanguage -= 1

            pag = 1
            requestUser = []
            print(proj['full_name'])

            while True:
                url = '{}{}{}{}'.format(proj['contributors_url'], '?per_page={}'.format(str(numeroContribuidores)), '&page={}'.format(pag), '&order=desc')
                request = [dev for dev in performRequest(url).json() if dev['type'] == 'User']
                requestUser += request
                pag += 1

                if len(request) == 0 or len(requestUser) > numeroContribuidores:
                    break

            contributors = [{'login': urlUser['login'], 'contributions': urlUser['contributions']} for urlUser in requestUser[:numeroContribuidores]]
            listDev += [contributor['login'] for contributor in contributors]
            print('Size -> ', len(contributors))
            listRepo[lang].append({proj['full_name']: contributors})

    print('Total Size -> ', len(listDev))
    file = open('{}{}'.format(path, '\\ProjWithUser.json'), 'w')
    json.dump(listRepo, file, indent=4)
    file.close()

    file = open('{}{}'.format(path, '\\devs.json'), 'w')
    json.dump(listDev, file, indent=4)
    file.close()

    return listDev


def devsByRepositorysLanguage(language, qtdDevelopersByRep, qtdRepositories):
    ignoreProjects = ['torvalds/linux', 'freeCodeCamp/freeCodeCamp', 'trekhleb/javascript-algorithms', 'airbnb/javascript']
    devList = getContributors(path, language, qtdDevelopersByRep, qtdRepositories, ignoreProjects)


if __name__ == '__main__':
    try:
        sys.argv[1]
    except IndexError:
        print('pass your github token as parameter ('
              'https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)')
        exit(1)

    # devList = ['rafaelfranca', 'eileencodes', 'lifo']

    path = '{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)), 'data')
    createFolderIfDoesntExist(path)
    devsByRepositorysLanguage(['JavaScript', 'Ruby', 'c'], 500, 5)
    f = open('data/ProjWithUser.json', )
    data = json.load(f)

    for lang in data:
        print(lang)
        numberContByLang = 0
        qtdCount = 0
        for repositories in data[lang]:
            numberContByRep = 0
            for rep in repositories:
                print('--', rep)
                for dev in repositories[rep]:
                    numberContByRep += dev['contributions']
                    # print('----', dev['contributions'])
                    # print('\n\n')
                print(numberContByRep)
                print('\n\n')
                numberContByLang += numberContByRep
            print(numberContByLang)
