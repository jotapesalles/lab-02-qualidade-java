import csv
import os
import subprocess
import statistics
import shutil

import list_repos


def clone_repo(url, repo_name):
    """Clona um único repositório."""
    repo_path = os.path.join("repos", repo_name)
    if not os.path.exists(repo_path):
        print(f"Clonando repositório: {repo_name}...")
        subprocess.run(["git", "clone", url + ".git", repo_path], check=True)
    return repo_path


def run_ck(repo_path, ck_repo_metrics_path):
    """Executa a ferramenta CK e retorna True se for bem-sucedido."""
    try:
        subprocess.run(
            ["java", "-jar", os.path.abspath("ck.jar"), os.path.abspath(repo_path), "false", "0"],
            cwd=ck_repo_metrics_path,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar CK: {e}")
        return False


def is_class_csv_valid(class_csv_path):
    """Verifica se o arquivo class.csv existe e contém mais do que apenas o cabeçalho."""
    if os.path.exists(class_csv_path):
        with open(class_csv_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            return len(rows) > 1  # Retorna True se houver mais de uma linha
    return False


def process_ck_metrics(repo_path, repo_name):
    """
    Executa a ferramenta CK para calcular as métricas de qualidade de um repositório.
    Verifica se o arquivo class.csv foi gerado corretamente e, se necessário, executa o CK novamente.
    """
    ck_repo_metrics_path = os.path.join("ck_metrics", repo_name)
    class_csv_path = os.path.join(ck_repo_metrics_path, "class.csv")

    # Cria o diretório de saída, se não existir
    if not os.path.exists(ck_repo_metrics_path):
        os.mkdir(ck_repo_metrics_path)

    # Executa o CK e verifica se o class.csv foi gerado corretamente
    print(f"Executando CK para análise de métricas em {repo_name}...")
    if run_ck(repo_path, ck_repo_metrics_path):
        if is_class_csv_valid(class_csv_path):
            print(f"Métricas CK salvas com sucesso em {ck_repo_metrics_path}")
        else:
            print(f"Arquivo {class_csv_path} está vazio ou contém apenas o cabeçalho. Executando CK novamente...")
            if run_ck(repo_path, ck_repo_metrics_path):
                if is_class_csv_valid(class_csv_path):
                    print(f"Métricas CK reexecutadas e salvas em {ck_repo_metrics_path}")
                else:
                    print(f"Erro: O arquivo {class_csv_path} ainda está vazio após reexecução.")
            else:
                print("Erro ao reexecutar CK.")
    else:
        print("Erro ao executar CK pela primeira vez.")

    return ck_repo_metrics_path


def media(numbers):
    """Calcula a média de uma lista de números."""
    return round(statistics.mean(numbers), 2) if numbers else 0


def mediana(numbers):
    """Calcula a mediana de uma lista de números."""
    return round(statistics.median(numbers), 2) if numbers else 0


def desvio_padrao(numbers):
    """Calcula o desvio padrão de uma lista de números."""
    return round(statistics.stdev(numbers), 2) if len(numbers) > 1 else 0


def calculate_metrics(repo_position, repo_name, ck_repo_metrics_path):
    """Calcula as métricas (média, mediana e desvio padrão) para um repositório."""
    csv_path = os.path.join(ck_repo_metrics_path, "class.csv")
    if not os.path.exists(csv_path):
        print(f"Arquivo de métricas não encontrado para {repo_name}.")
        repo_path = os.path.join("repos", repo_name)
        process_ck_metrics(repo_path, repo_name)

    print(f"Lendo métricas de qualidade para {repo_name}...")
    with open(csv_path, "r", encoding="utf-8") as ck_file:
        reader = csv.reader(ck_file)
        next(reader)  # Pula cabeçalho

        # Inicializa as listas de métricas
        cbo_list, dit_list, lcom_list = [], [], []

        # Processa cada linha do CSV
        for row in reader:
            cbo, dit, lcom = int(row[3]), int(row[8]), int(row[11])
            cbo_list.append(cbo)
            dit_list.append(dit)
            lcom_list.append(lcom)

    # Calcula as métricas
    return {
        "Popularidade": repo_position,
        "Nome": repo_name,
        "CBO_Média": media(cbo_list),
        "CBO_Mediana": mediana(cbo_list),
        "CBO_Desvio_Padrão": desvio_padrao(cbo_list),
        "DIT_Média": media(dit_list),
        "DIT_Mediana": mediana(dit_list),
        "DIT_Desvio_Padrão": desvio_padrao(dit_list),
        "LCOM_Média": media(lcom_list),
        "LCOM_Mediana": mediana(lcom_list),
        "LCOM_Desvio_Padrão": desvio_padrao(lcom_list)
    }


def delete_dir(dir_path):
    """Apaga o diretório criado após o processamento."""
    if os.path.exists(dir_path):
        print(f"Apagando diretório {dir_path}...")
        shutil.rmtree(dir_path)
        print(f"Repositório {dir_path} apagado.")


def is_repo_processed(repo_name, output_file):
    """Verifica se o repositório já foi processado e está no arquivo de saída."""
    if not os.path.exists(output_file):
        return False

    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[1] == repo_name:
                return True
    return False


def append_metrics_to_csv(metrics, output_file):
    """Adiciona as métricas de um repositório ao arquivo CSV de saída."""
    file_exists = os.path.exists(output_file)
    with open(output_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Popularidade", "Nome", "CBO_Média", "CBO_Mediana", "CBO_Desvio_Padrão",
            "DIT_Média", "DIT_Mediana", "DIT_Desvio_Padrão",
            "LCOM_Média", "LCOM_Mediana", "LCOM_Desvio_Padrão"
        ])
        if not file_exists:
            writer.writeheader()  # Escreve o cabeçalho se o arquivo não existir
        writer.writerow(metrics)


def main():
    list_repos.main()

    # Cria diretórios necessários
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists("ck_metrics"):
        os.mkdir("ck_metrics")

    # Arquivo de saída
    output_file = "quality_metrics.csv"

    # Lista de repositórios a serem processados
    with open("process_metrics.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pula cabeçalho

        # Processa cada repositório
        for row in reader:
            posicao, nome, dono, estrelas, releases, criado_em, url = row

            # Verifica se o repositório já foi processado (no arquivo CSV)
            if is_repo_processed(nome, output_file):
                print(f"Repositório {nome} já foi processado. Pulando...")
                continue

            # Verifica se o repositório já existe na pasta ck_metrics
            ck_repo_metrics_path = os.path.join("ck_metrics", nome)
            if os.path.exists(ck_repo_metrics_path):
                print(f"Repositório {nome} já existe em ck_metrics. Processando métricas...")
                # Apenas processa as métricas, sem executar o CK novamente
                metrics = calculate_metrics(posicao, nome, ck_repo_metrics_path)
                if metrics:
                    append_metrics_to_csv(metrics, output_file)
                    print(f"Métricas de {nome} adicionadas ao arquivo {output_file}.")
                    delete_dir(ck_repo_metrics_path)
                continue

            # Se não existir em ck_metrics, clona o repositório e executa o CK
            repo_path = clone_repo(url, nome)
            ck_repo_metrics_path = process_ck_metrics(repo_path, nome)

            # Calcula as métricas
            metrics = calculate_metrics(posicao, nome, ck_repo_metrics_path)
            if metrics:
                # Adiciona as métricas ao arquivo CSV
                append_metrics_to_csv(metrics, output_file)
                print(f"Métricas de {nome} adicionadas ao arquivo {output_file}.")

            # Apaga o repositório clonado (se foi clonado)
            if os.path.exists(repo_path):
                delete_dir(repo_path)

    print("Processo concluído!")


if __name__ == "__main__":
    main()
