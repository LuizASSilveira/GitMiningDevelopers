from pprint import pprint

from src.userGitHubInfo import getUserInfo, getUserInfByMonth, getUserInfByYear, repositoryUser, getUserRepositoryCommit, userCommitDiffInfo
from src.utils import developerOverviewAux, saveCSV, jsonPrettify, saveDictCSV, saveJson, createFolderIfDoesntExist
from src.selectContributors import getContributors
import pandas as pd
import numpy as np
import json
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
        for index in range(len(keys)):
            devCollections[keys[index]][loginDev] = dict(
                zip(list(devInfByMonth.keys()), np.array(list(devInfByMonth.values()))[:, index]))

    for key in devCollections.keys():
        pd.set_option('display.max_columns', 29)
        df = pd.DataFrame.from_dict(devCollections[key], orient='index').fillna(0).astype('int64')
        df.rename(columns={'Unnamed: 0': 'Developer'}, inplace=True)
        df = df[[df.columns[0]] + df.columns[1:].sort_values(key=lambda x: pd.to_datetime(x, format='%Y/%m')).tolist()]
        df.to_csv('{}{}.csv'.format(standardDirectory, key))


def assisAvg(dataDevCollection, inManyYears):
    dataDevCollection['totalRepositoriesWithContributedPullRequestReviews'] = dataDevCollection['totalRepositoriesWithContributedPullRequestReviews']/inManyYears
    dataDevCollection['totalRepositoriesWithContributedPullRequests'] = dataDevCollection['totalRepositoriesWithContributedPullRequests']/inManyYears
    dataDevCollection['totalRepositoriesWithContributedCommits'] = dataDevCollection['totalRepositoriesWithContributedCommits']/inManyYears
    dataDevCollection['totalRepositoriesWithContributedIssues'] = dataDevCollection['totalRepositoriesWithContributedIssues']/inManyYears
    return dataDevCollection


def devInfoMining(standardDirectory, listDev):
    devInfos = []
    errorNoneGit = {}

    for loginDev in listDev:
        print(loginDev)

        createFolderIfDoesntExist(standardDirectory)

        devInfo = getUserInfo(loginDev)
        userInfoByYear, keys, inManyYears = getUserInfByYear(loginDev, devInfo['data']['user']['createdAt'])
        userInfoAllTime = pd.DataFrame.from_dict(userInfoByYear, orient='index', columns=keys).sum(axis=0)
        userInfoAllTime = assisAvg(userInfoAllTime, inManyYears)

        OWNER, COLLABORATOR = repositoryUser(loginDev)
        repositories = {
            'owner': OWNER,
            'collaborator': COLLABORATOR
        }

        userId = devInfo['data']['user']['id']
        userCommits = getUserRepositoryCommit(userId, repositories['owner'] + repositories['collaborator'])
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

        userFolder = '{}{}\\'.format(standardDirectory, loginDev)
        createFolderIfDoesntExist(userFolder)
        saveJson(userCommits, '{}{}'.format(userFolder, 'userCommit.json'))

        # print(userCommits)

        print(userCommitInfo)
        developerOverview = developerOverviewAux(devInfo, repositories, userInfoAllTime, userCommitInfo)
        devInfos.append(developerOverview)

    print('\n\nNone Error Git --> ', errorNoneGit)

    standardDirectory = '{}\\{}\\'.format(standardDirectory, 'generalInformation')
    createFolderIfDoesntExist(standardDirectory)

    saveCSV(devInfos, standardDirectory + 'devInfos.csv')
    # userCommitDiffInfo(userCommits)


if __name__ == '__main__':
    try:
        sys.argv[1]
    except IndexError:
        print('pass your github token as parameter ('
              'https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)')
        exit(1)

    path = '{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)), 'data')
    createFolderIfDoesntExist(path)

    devList = ['rafaelfranca', 'eileencodes', 'lifo']
    # devList = json.load(open('data/devs.json', ))

    devInfoMining(path, devList)
    # devContributionsCollection(path, devList)
