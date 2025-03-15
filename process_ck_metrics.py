import csv
import os
import subprocess
def process_ck_metrics():

    if not os.path.exists("ck_metrics"):
        os.mkdir("ck_metrics")
        
    for repo in os.listdir("repos"):
        repo_path = os.path.join("repos", repo)
        
        if os.path.exists(repo_path):
            ck_repo_metrics_path = os.path.join("ck_metrics", repo)
            if not os.path.exists(ck_repo_metrics_path):
                os.mkdir(ck_repo_metrics_path)
                print(f"Executando CK para análise de métricas em {repo}...")
                try:
                    subprocess.run(
                        ["java", "-jar", os.path.abspath("ck.jar"), os.path.abspath(repo_path), "false", "0"], 
                        cwd=ck_repo_metrics_path,
                        check=True
                    )
                    print(f"Métricas CK salvas em {ck_repo_metrics_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao executar CK em {repo}: {e}")

def process_ck_results():
    
    print("Processando resultados da análise CK...")
    with open("ck_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Projeto", "Classe", "CBO", "DIT", "LCOM"])
        
        for repo in os.listdir("ck_metrics"):
            csv_path = os.path.join("ck_metrics", repo, "class.csv")
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
    process_ck_metrics()
    print("Análise concluída! Verifique ck_metrics para os resultados.")
