from src.userGitHubInfo import getUserInfo, getUserInfByYear, repositoryUser, getUserRepositoryCommit, userCommitDiffInfo, getContributors
from src.fileAnalyze import saveJson
import pandas as pd
import json
import sys
import os


def jsonPrettify(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def saveCSV(data, path):
    pd.json_normalize(data).to_csv(path)


def saveDictCSV(data, orient, columns, path):
    pd.DataFrame.from_dict(data, orient=orient, columns=columns).to_csv(path)


def developerOverviewAux(userInfo, repositories, userInfoAllTime, userCommitInfo):
    developerOverview = {
        "login": userInfo['data']['user']['login'],
        "nome": userInfo['data']['user']['name'],
        "email": userInfo['data']['user']['email'],
        "dataCriacaoContaGithub": userInfo['data']['user']['createdAt'],
        "location": userInfo['data']['user']['location'],

        "company": userInfo['data']['user']['company'],
        "watching": userInfo['data']['user']['watching']['totalCount'],
        "followers": userInfo['data']['user']['followers']['totalCount'],
        "following": userInfo['data']['user']['following']['totalCount'],
        "organizations": userInfo['data']['user']['organizations']['totalCount'],

        "projects": userInfo['data']['user']['projects']['totalCount'],
        "repositories": userInfo['data']['user']['repositories']['totalCount'],
        "repositoriesOwner": len(repositories['owner']),
        "repositoriesCollaborator": len(repositories['collaborator']),

        "pullRequests": userInfo['data']['user']['pullRequests']['totalCount'],
        "issues": userInfo['data']['user']['issues']['totalCount'],
        "gists": userInfo['data']['user']['gists']['totalCount'],

        "commitComments": userInfo['data']['user']['commitComments']['totalCount'],
        "issueComments": userInfo['data']['user']['issueComments']['totalCount'],
        "gistComments": userInfo['data']['user']['gistComments']['totalCount'],

        "totalIssueContributions": userInfoAllTime['totalIssueContributions'],
        "totalCommitContributions": userInfoAllTime['totalCommitContributions'],
        "totalRepositoryContributions": userInfoAllTime['totalRepositoryContributions'],
        "totalPullRequestContributions": userInfoAllTime['totalPullRequestContributions'],
        "totalPullRequestReviewContributions": userInfoAllTime['totalPullRequestReviewContributions'],
        "totalRepositoriesWithContributedIssues": userInfoAllTime['totalRepositoriesWithContributedIssues'],
        "totalRepositoriesWithContributedCommits": userInfoAllTime['totalRepositoriesWithContributedCommits'],
        "totalRepositoriesWithContributedPullRequests": userInfoAllTime['totalRepositoriesWithContributedPullRequests'],
        "totalRepositoriesWithContributedPullRequestReviews": userInfoAllTime['totalRepositoriesWithContributedPullRequestReviews'],

        'totalChangedFiles': userCommitInfo['changedFiles'],
        'totalAdditions': userCommitInfo['additions'],
        'totalDeletions': userCommitInfo['deletions']
    }
    return developerOverview


def main(standardDirectory, listDev):
    devInfos = []

    for loginUser in listDev:

        # standardDirectory += loginUser
        # if not os.path.exists(standardDirectory):
        #     os.mkdir(standardDirectory)

        print('\n\n\n\n\n')
        print('Login User', loginUser)
        print('---------------')
        print('\tuserInfo')
        print('---------------')

        userInfo = getUserInfo(loginUser)
        userInfoByYear, keys = getUserInfByYear(loginUser, userInfo['data']['user']['createdAt'])
        userInfoAllTime = pd.DataFrame.from_dict(userInfoByYear, orient='index', columns=keys).sum(axis=0)

        print('---------------')
        print('repositoryUser')
        print('---------------')
        OWNER, COLLABORATOR = repositoryUser(loginUser)
        repositories = {
            'owner': OWNER,
            'collaborator': COLLABORATOR
        }

        print('---------------')
        print('getUserRepositoryCommit')
        print('---------------')
        userId = userInfo['data']['user']['id']
        userCommits = getUserRepositoryCommit(userId, repositories['owner']+repositories['collaborator'])
        userCommitInfo = {
            'changedFiles': 0,
            'additions': 0,
            'deletions': 0
        }
        for commit in userCommits:
            userCommitInfo['changedFiles'] += commit['changedFiles']
            userCommitInfo['additions'] += commit['additions']
            userCommitInfo['deletions'] += commit['deletions']

        print(userCommitInfo)
        developerOverview = developerOverviewAux(userInfo, repositories, userInfoAllTime, userCommitInfo)
        devInfos.append(developerOverview)
    saveCSV(devInfos, standardDirectory+'\\devInfos.csv')

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
    # devList = ['rafaelfranca']
    # devList = ['spastorino']
    path = 'C:\\Users\\luiz_\\Desktop\\data'
    devList = getContributors()
    main(path, devList)
