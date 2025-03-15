import csv
import os
import subprocess

def clone_repos():
    if not os.path.exists("repos"):  
        os.mkdir("repos")
    
    with open("repos_java.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            nome, dono, estrelas, releases, criado_em, url = row
            repo_path = os.path.join("repos", nome)
            
            if not os.path.exists(repo_path):
                print(f"Clonando repositório: {nome}...")
                subprocess.run(["git", "clone", url+".git", repo_path])

if __name__ == "__main__":
    clone_repos()
    print("Análise concluída! Verifique ck_results.csv para os resultados.")
