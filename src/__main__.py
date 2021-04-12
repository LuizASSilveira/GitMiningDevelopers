from src.userGitHubInfo import getUserInfo, getUserInfByMonth, getUserInfByYear, repositoryUser, getUserRepositoryCommit, userCommitDiffInfo, getContributors
from src.utils import developerOverviewAux, saveCSV, jsonPrettify, saveDictCSV
import pandas as pd
import numpy as np
import sys
import os


def devContributionsCollection(standardDirectory, listDev):
    devCollections = {
        'totalIssueContributions': {},
        'totalCommitContributions': {},
        'totalRepositoryContributions': {},
        'totalPullRequestContributions': {},
        'totalPullRequestReviewContributions': {},
        'totalRepositoriesWithContributedIssues': {},
        'totalRepositoriesWithContributedCommits': {},
        'totalRepositoriesWithContributedPullRequests': {},
        'totalRepositoriesWithContributedPullRequestReviews': {}
    }

    for loginDev in listDev:
        devInfo = getUserInfo(loginDev)
        devInfByMonth, keys = getUserInfByMonth(loginDev, devInfo['data']['user']['createdAt'])
        print(keys)

        for index in range(len(keys)):
            devCollections[keys[index]][loginDev] = dict(zip(devInfByMonth.keys(), np.array(list(devInfByMonth.values()))[:, index]))

    print(pd.DataFrame.from_dict(devCollections['totalIssueContributions'], orient='index'))

    for key in devCollections.keys():
        pd.DataFrame.from_dict(devCollections[key], orient='index').to_csv('{}{}.csv'.format(standardDirectory, key))


def main(standardDirectory, listDev):
    devInfos = []
    errorNoneGit = {}

    for loginDev in listDev:
        print(loginDev)

        if not os.path.exists(standardDirectory):
            os.mkdir(standardDirectory)

        devInfo = getUserInfo(loginDev)
        userInfoByYear, keys = getUserInfByYear(loginDev, devInfo['data']['user']['createdAt'])
        userInfoAllTime = pd.DataFrame.from_dict(userInfoByYear, orient='index', columns=keys).sum(axis=0)

        OWNER, COLLABORATOR = repositoryUser(loginDev)
        repositories = {
            'owner': OWNER,
            'collaborator': COLLABORATOR
        }

        userId = devInfo['data']['user']['id']
        userCommits = getUserRepositoryCommit(userId, repositories['owner'] + repositories['collaborator'])
        # userCommits = getUserRepositoryCommit(userId, repositories['collaborator'])
        userCommitInfo = {
            'changedFiles': 0,
            'additions': 0,
            'deletions': 0
        }

        for index, commit in enumerate(userCommits):
            if not commit:
                errorNoneGit[index] = commit
                continue
            userCommitInfo['changedFiles'] += commit['changedFiles'] if commit['changedFiles'] else 0
            userCommitInfo['additions'] += commit['additions'] if commit['additions'] else 0
            userCommitInfo['deletions'] += commit['deletions'] if commit['deletions'] else 0

        print(userCommitInfo)

        developerOverview = developerOverviewAux(devInfo, repositories, userInfoAllTime, userCommitInfo)
        devInfos.append(developerOverview)
    print(errorNoneGit)
    saveCSV(devInfos, standardDirectory+'devInfos.csv')

        # userCommitDiffInfo(userCommits)
        # saveCSV(developerOverview, standardDirectory + '\\developerOverview.csv')
        # saveDictCSV(userInfoByYear, 'index', keys, standardDirectory + '\\userInfoByYearTet.csv')


if __name__ == '__main__':
    try:
        sys.argv[1]
    except IndexError:
        print('Please, set the GITHUB_TOKEN environment variable with your OAuth token ('
              'https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)')
        exit(1)

    # devList = ['QuincyLarson']
    devList = ['rafaelfranca', 'eileencodes']
    # devList = ['eileencodes']
    # devList = ['maclover7']
    # path = 'C:\\Users\\luiz_\\Desktop\\data'
    path = 'C:\\Users\\luiz\\Desktop\\data\\'
    # devList = getContributors()
    # main(path, devList)
    devContributionsCollection(path, devList)
