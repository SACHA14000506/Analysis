
import json
import math
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import sys
import csv

# load token
load_dotenv('token.env')
token = os.getenv('GITHUB_TOKEN')

if token is None:
    print("GITHUB_TOKEN is not set in the environment", file=sys.stderr)
    raise SystemExit(1)

# valeurs par default
nproprio = ""
repo = ""

# const and variables
BASE_URL = f"https://api.github.com/"
NUMBER_RES = 30

def convert_date_format(date_str):

    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    new_date_str = dt.strftime('%Y-%m-%dT%H:%M:%S.%f+0000')
    
    return new_date_str

def read_keywords_from_csv(file_path):
    keywords = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            keywords.extend(row)  
    return keywords

def getRepoId(owner, repo):
    query = f"repo:{owner}/{repo}"
    response = requests.get(
        f"{BASE_URL}search/repositories?q={query}&per_page=1",
        headers={'Authorization': f'token {token}'}
    )

    if response.status_code == 200:
        result = response.json()
        if result['total_count'] > 0:
            return result['items'][0]['id']
    return 0

def findAllBugs(proprio, nomRepo, keywords):
    currentBugs = 0
    listIssues = []

    for keyword in keywords:
        page = 1
        maxPage = 1
        while page <= maxPage:
            verifQuery = f"repo:{proprio}/{nomRepo}+is:issue+is:closed+{keyword}&page={page}"
            responseVerif = requests.get(
                f"{BASE_URL}search/issues?q={verifQuery}",
                headers={'Authorization': f'token {token}'}
            )

            responseCountJson = responseVerif.json()

            if page == 1:
                currentBugs += responseCountJson["total_count"]
                maxPage = math.ceil(currentBugs / NUMBER_RES)

            page += 1

            bugs = responseCountJson.get("items", [])
            for bug in bugs:
                id = bug["number"]
                dateCreation = convert_date_format(bug["created_at"])
                dateFermeture = convert_date_format(bug["closed_at"])

                key = f"{nomRepo}-{id}"
                issue = {"key": key, "fields": {"created": dateCreation, "resolutiondate": dateFermeture}}
                listIssues.append(issue)

            print(f"Lecture de la page {page-1} pour les bogues fermés avec le mot-clé : {keyword}")
            time.sleep(2.5)

    print(f"Il y a {currentBugs} bogues résolus dans le projet {proprio}/{nomRepo} !!! :O")
    resultat = {
        "expand": "schema, names",
        "startAt": 0,
        "maxResults": currentBugs,
        "total": currentBugs,
        "issues": listIssues
    }
    return resultat

def execution(proprio, nomRepo):
    keywords = read_keywords_from_csv('key.csv')  # 读取关键字
    contenu = findAllBugs(proprio=proprio, nomRepo=nomRepo, keywords=keywords)

    if not os.path.exists("fetch_issues"):
        os.makedirs("fetch_issues")

    with open("fetch_issues/res0.json", 'w') as ecriture:
        json.dump(contenu, ecriture)

##############################################################################

# lecture des paramètres
if len(sys.argv) < 3:
    print("Veuillez indiquer le pseudo du propriétaire et le nom du répertoire svp")
    print("python fetch_alternative.py <propriétaire> <répertoire>")
    sys.exit(0)
else:
    nproprio = sys.argv[1]
    repo = sys.argv[2]

# appel
execution(nproprio, repo)

