import requests
import time


def requestApiGitHubV4(query, headers, variables={}, numTentativa=20):
    while numTentativa > 0:
        try:
            request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables},
                                    headers=headers, timeout=30)
            if request.status_code == 200:
                return request.json()
            else:
                print('Tentativa Request Api V4 GitHub n° ' + str(20 - numTentativa + 1))
                if 'timeout' in request.json()["errors"][0]["message"]:
                    raise Exception
                numTentativa -= 1
                time.sleep(3)
        except:
            if numTentativa < 17:
                variables["numPage"] = (variables["numPage"] - 10) if variables["numPage"] > 10 else 10
    print(query)
    return {}