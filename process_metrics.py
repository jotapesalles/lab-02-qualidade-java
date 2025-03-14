import requests
import json
import csv

# Configurações
GITHUB_TOKEN = "SEU_TOKEN_AQUI"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
QUERY = """
{
  search(query: "language:Java", type: REPOSITORY, first: 10) {
    nodes {
      ... on Repository {
        name
        owner {
          login
        }
        stargazers {
          totalCount
        }
        releases {
          totalCount
        }
        createdAt
        url
      }
    }
  }
}
"""

def fetch_repositories():
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": QUERY}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["data"]["search"]["nodes"]
    else:
        print("Erro ao buscar dados:", response.text)
        return []

def save_to_csv(repos):
    with open("repositorios_java.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nome", "Dono", "Estrelas", "Releases", "Criado em", "URL"])
        for repo in repos:
            writer.writerow([repo["name"], repo["owner"]["login"], repo["stargazers"]["totalCount"], 
                             repo["releases"]["totalCount"], repo["createdAt"], repo["url"]])

if __name__ == "__main__":
    repositories = fetch_repositories()
    if repositories:
        save_to_csv(repositories)
        print("Dados salvos em repositorios_java.csv")
    else:
        print("Nenhum dado coletado.")
