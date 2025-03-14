import requests
import json
import csv
import os
import subprocess

# Configurações
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
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
        sshUrl
      }
    }
  }
}
"""

def fetch_repositories():
    print("Buscando repositórios Java populares no GitHub...")
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": QUERY}, headers=HEADERS)
    if response.status_code == 200:
        print("Repositórios encontrados com sucesso!")
        return response.json()["data"]["search"]["nodes"]
    else:
        print("Erro ao buscar dados:", response.text)
        return []

def save_to_csv(repos):
    print("Salvando dados dos repositórios em CSV...")
    with open("repositorios_java.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nome", "Dono", "Estrelas", "Releases", "Criado em", "URL", "SSH URL"])
        for repo in repos:
            writer.writerow([repo["name"], repo["owner"]["login"], repo["stargazers"]["totalCount"], 
                             repo["releases"]["totalCount"], repo["createdAt"], repo["url"], repo["sshUrl"]])
    print("Dados salvos em repositorios_java.csv")

def clone_and_analyze():
    if not os.path.exists("repositorios"):  
        os.mkdir("repositorios")
    
    with open("repositorios_java.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pula cabeçalho
        for row in reader:
            nome, dono, estrelas, releases, criado_em, url, ssh_url = row
            repo_path = os.path.join("repositorios", nome)
            
            if not os.path.exists(repo_path):
                print(f"Clonando repositório: {nome}...")
                subprocess.run(["git", "clone", ssh_url, repo_path])
            
            print(f"Executando CK para análise de métricas em {nome}...")
            subprocess.run(["java", "-jar", "ck.jar", repo_path, "false", "0"])  

def process_ck_results():
    print("Processando resultados da análise CK...")
    with open("ck_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Projeto", "Classe", "CBO", "DIT", "LCOM"])
        
        for repo in os.listdir("repositorios"):
            csv_path = os.path.join("repositorios", repo, "class.csv")
            if os.path.exists(csv_path):
                print(f"Lendo métricas de qualidade para {repo}...")
                with open(csv_path, "r", encoding="utf-8") as ck_file:
                    reader = csv.reader(ck_file)
                    next(reader)  # Pula cabeçalho
                    for row in reader:
                        class_name, cbo, dit, lcom = row[0], row[5], row[6], row[8]
                        writer.writerow([repo, class_name, cbo, dit, lcom])
    print("Resultados processados e salvos em ck_results.csv")

if __name__ == "__main__":
    repositories = fetch_repositories()
    if repositories:
        save_to_csv(repositories)
        clone_and_analyze()
        process_ck_results()
        print("Análise concluída! Verifique ck_results.csv para os resultados.")
    else:
        print("Nenhum dado coletado.")
