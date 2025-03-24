import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Configuração do estilo
sns.set_theme(style="whitegrid")

# Carregar os dados
process_metrics_path = "process_metrics.csv"
quality_metrics_path = "quality_metrics.csv"

process_df = pd.read_csv(process_metrics_path)
quality_df = pd.read_csv(quality_metrics_path)

# Renomear colunas
process_df.rename(columns={
    "Estrelas": "stars",
    "Releases": "releases",
    "Tamanho (KB)": "size",
    "Criado em": "created_at"
}, inplace=True)

quality_df.rename(columns={
    "CBO_Média": "CBO",
    "DIT_Média": "DIT",
    "LCOM_Média": "LCOM"
}, inplace=True)

# Converter data de criação para idade do repositório
process_df["created_at"] = pd.to_datetime(process_df["created_at"])
today = pd.Timestamp.now(tz='UTC') 
process_df["age"] = (today - process_df["created_at"]).dt.days / 365.25

# 📌 Popularidade x Qualidade
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)

merged_df = pd.merge(process_df, quality_df, on="Nome", how="inner")

sns.regplot(x=merged_df["stars"], y=merged_df["CBO"], scatter_kws={'alpha': 0.5})

plt.xscale("log")  # Popularidade pode ter valores muito desbalanceados
plt.xlabel("Número de Estrelas (log)")
plt.ylabel("CBO (Acoplamento)")
plt.title("Popularidade vs CBO")

plt.subplot(1, 2, 2)
sns.regplot(x=merged_df["stars"], y=merged_df["LCOM"], scatter_kws={'alpha':0.5})
plt.xscale("log")
plt.xlabel("Número de Estrelas (log)")
plt.ylabel("LCOM (Falta de Coesão)")
plt.title("Popularidade vs LCOM")

plt.tight_layout()
plt.savefig("grafico1.png")
plt.close()

# 📌 Maturidade x Qualidade (DIT)
plt.figure(figsize=(6, 4))
sns.regplot(x=merged_df["age"], y=merged_df["DIT"], scatter_kws={'alpha':0.5})
plt.xlabel("Idade do Repositório (anos)")
plt.ylabel("DIT (Profundidade de Herança)")
plt.title("Maturidade vs DIT")
plt.savefig("grafico2.png")
plt.close()

# 📌 Atividade x Qualidade (LCOM)
plt.figure(figsize=(6, 4))
sns.regplot(x=merged_df["releases"], y=merged_df["LCOM"], scatter_kws={'alpha':0.5})
plt.xlabel("Número de Releases (Atividade)")
plt.ylabel("LCOM (Coesão)")
plt.title("Atividade vs LCOM")
plt.savefig("grafico3.png")
plt.close()

# 📌 Tamanho x Qualidade (CBO e LCOM)
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.regplot(x=merged_df["size"], y=merged_df["CBO"], scatter_kws={'alpha':0.5})
plt.xscale("log")
plt.xlabel("Tamanho KB (log)")
plt.ylabel("CBO (Acoplamento)")
plt.title("Tamanho vs CBO")

plt.subplot(1, 2, 2)
sns.regplot(x=merged_df["size"], y=merged_df["LCOM"], scatter_kws={'alpha':0.5})
plt.xscale("log")
plt.xlabel("Tamanho KB (log)")
plt.ylabel("LCOM (Coesão)")
plt.title("Tamanho vs LCOM")

plt.tight_layout()
plt.savefig("grafico4.png")
plt.close()
