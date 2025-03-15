# Análise de Qualidade de Código Java com CK

## Visão Geral
Este projeto coleta e analisa métricas de qualidade de código-fonte de repositórios Java hospedados no GitHub. Utiliza a API GraphQL do GitHub para buscar os repositórios mais populares e a ferramenta CK para extrair métricas de qualidade do código.

## Funcionalidades
- **Coleta de repositórios**: Obtém os 1000 repositórios Java mais populares do GitHub.
- **Armazenamento dos dados**: Salva as informações dos repositórios em um arquivo CSV.
- **Clonagem dos repositórios**: Baixa o código-fonte localmente.
- **Execução da ferramenta CK**: Analisa métricas de qualidade do código.
- **Processamento dos resultados**: Consolida os dados das métricas e gera um relatório CSV.

## Pré-requisitos
Antes de executar o projeto, você precisa instalar:
- **Python 3.x**
- **Git**
- **Java (JDK 8 ou superior)**
- **Ferramenta CK** (Baixar o `ck.jar` do [repositório oficial](https://github.com/mauricioaniche/ck))

## Configuração
1. Obtenha um token do GitHub e substitua `SEU_TOKEN_AQUI` no código.
2. Certifique-se de que o arquivo `ck.jar` está no mesmo diretório do script.

## Como Executar
1. Clone este repositório:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```
2. Instale as dependências Python:
   ```sh
   pip install requests
   ```
3. Execute o script principal:
   ```sh
   python main.py
   ```
4. Após a execução, os seguintes arquivos serão gerados:
   - `repositorios_java.csv`: Lista dos repositórios coletados.
   - `ck_results.csv`: Resultados da análise de métricas.

## Estrutura do Projeto
```
/
├── main.py          # Script principal
├── colect_repos.py  # Script para coletar os repositórios
├── ck.jar            # Ferramenta CK
├── repositorios/     # Diretório onde os repositórios serão clonados
├── repositorios_java.csv  # Lista dos repositórios coletados
├── ck_results.csv    # Resultados da análise
└── README.md         # Este arquivo
```

## Métricas de Qualidade Coletadas
- **CBO (Coupling Between Objects)**: Acoplamento entre objetos.
- **DIT (Depth of Inheritance Tree)**: Profundidade da árvore de herança.
- **LCOM (Lack of Cohesion of Methods)**: Falta de coesão dos métodos.

## Autor
- João Paulo de Sales Pimenta
- Enzo
- Igor


