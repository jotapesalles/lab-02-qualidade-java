import requests
from dotenv import load_dotenv
import csv
import os

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_query(after_cursor=None, first=10):
    after = f', after: "{after_cursor}"' if after_cursor else ''
    return f"""
    {{
      search(query: "language:Java", type: REPOSITORY, first: {first}{after}) {{
        edges {{
          cursor
          node {{
            ... on Repository {{
              name
              owner {{
                login
              }}
              stargazers {{
                totalCount
              }}
              releases {{
                totalCount
              }}
              createdAt
              url
              diskUsage
            }}
        }}
      }}
      pageInfo {{
        hasNextPage
        endCursor
      }}
    }}
    }}"""


def fetch_repositories(target_count=1000):
    print("Coleta dados de repositórios do GitHub.")
    repos = []
    after_cursor = None
    consulta = 1

    while len(repos) < target_count:
        print(f"Consulta #{consulta} com after_cursor: {after_cursor}")
        response = requests.post(GITHUB_GRAPHQL_URL, json={"query": get_query(after_cursor)}, headers=HEADERS)
        if response.status_code == 200:
            search_data = response.json()["data"]["search"]
            nodes = [edge["node"] for edge in response.json()["data"]["search"]["edges"]]
            repos.extend(nodes)
            after_cursor = search_data['pageInfo']['endCursor']
            consulta += 1
        else:
            print("Erro ao buscar dados:", response.text)
            break
    print(f"Total de repositórios coletados: {len(repos)}")
    return repos

def save_to_csv(repos):
    with open("process_metrics.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Adiciona o cabeçalho com o campo "Posição"
        writer.writerow(["Posição", "Nome", "Dono", "Estrelas", "Releases", "Criado em", "Tamanho (KB)", "URL"])
        
        # Itera sobre a lista de repositórios com enumerate para obter a posição
        for posicao, repo in enumerate(repos, start=1):
            writer.writerow([
                posicao,
                repo["name"],
                repo["owner"]["login"],
                repo["stargazers"]["totalCount"],
                repo["releases"]["totalCount"],
                repo["createdAt"],
                repo["diskUsage"],
                repo["url"]
            ])

def main():
    repos_java_path = os.path.join("process_metrics.csv")
    if not os.path.exists(repos_java_path):
      repositories = fetch_repositories()
      if repositories:
          save_to_csv(repositories)
          print("Dados salvos em process_metrics.csv")
      else:
          print("Nenhum dado coletado.")
    else:
      print("Repositórios já listados.")
      
if __name__ == "__main__":
    main()
