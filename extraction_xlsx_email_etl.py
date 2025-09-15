#Script para extração de arquivo xlsx ou csv anexo em email, tratamento e disponbilização de arquivo em path-sharepoint
# %%
import win32com.client as win32
from pathlib import Path
from datetime import datetime

# %%


# Caminho base para salvar os anexos
destino = Path(r"path_aqui")
destino.mkdir(parents=True, exist_ok=True)

# Gera a data atual no formato AAAA-MM-DD
data_hoje = datetime.now().strftime("%Y-%m-%d")

# Nome fixo do arquivo com data
nome_arquivo_destino = f"pendente_cliente_{data_hoje}.xlsx"  # ajuste a extensão conforme necessário

# Conectar ao Outlook
outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # Caixa de entrada
messages = inbox.Items
messages.Sort("[ReceivedTime]", True)  # Ordena por data mais recente

# Filtros
sender_email = "email address"
assunto_desejado = "subject"

# Percorre os e-mails até encontrar o mais recente que corresponde
for message in messages:
    try:
        if message.Class != 43:
            continue

        remetente = message.SenderEmailAddress
        assunto = message.Subject

        if sender_email in remetente or assunto_desejado in assunto:
            attachments = message.Attachments

            for att in attachments:
                caminho_arquivo = destino / nome_arquivo_destino
                att.SaveAsFile(str(caminho_arquivo))
                print(f"Anexo salvo como: {caminho_arquivo}")

            break  # Para o loop após salvar o anexo mais recente

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


# %%
import pandas as pd

# %%
data_hoje = datetime.now().strftime("%Y-%m-%d")
caminho_arquivo = Path(fr"caminho_arquivo_{data_hoje}.xlsx")
#""


# %%
arquivo= pd.read_excel(caminho_arquivo)

# %%
arquivo

# %%
# 1. Excluir as 12 primeiras linhas e 5 últimas
arquivo=arquivo.iloc[11:-5].reset_index(drop=True)


# %%
arquivo.drop(columns=['Unnamed: 0'],inplace=True)

# %%
arquivo.columns=arquivo.iloc[0] #primeira linha como cabeçalho
arquivo= arquivo[1:].reset_index(drop=True)

# %%
arquivo

# %%
#tratar a coluna data 
coluna_data='Data Inicio da Fase'

# %%
arquivo[coluna_data]=pd.to_datetime(arquivo[coluna_data], dayfirst=True)
arquivo[coluna_data]=arquivo[coluna_data].dt.strftime("%Y-%m-%d %H:%M")

# %%
linhas=len(arquivo)


# %%
print(linhas)

# %%
arquivo.rename(columns={'NaN': 'Coluna1'},inplace=True)
arquivo.rename(columns={'CPF/CNPJ': 'CPFCNPJ'},inplace=True)

# %%
caminho_csv= destino / f"PendentesOnboardingClientes.csv"
arquivo.to_csv(caminho_csv, index=False, sep=',')
print(f"Arquivo salvo em:{caminho_csv}")

# %%
sharepoint_pasta=Path(r"caminho_sharepoint")

# %
arquivo.to_csv(sharepoint_pasta / f"PendentesOnboardingClientes2.csv",index=False, sep="," )


 
