# Analisa os motivos unicos de transação negadas, limpa qtd de colunas e salva a base no path df_resultados_trxs
# %%
import pandas as pd
 
base_trxs = r"N:\DRSC\GRCF\GRF\Trxs_202408.csv"


 


# %%
valores_trxs = set()  # Usar um conjunto para garantir unicidade na MotivoAutorizacaoNegada
chunksize = 100_000
resultados = []

# %%
for chunk in pd.read_csv(base_trxs, sep=';', encoding='utf-8', chunksize=chunksize, low_memory=False):
    # Filtrar as linhas onde Modalidade == 'CNP'
    chunk_filtrado = chunk.loc[chunk['TpEntryMode'] == 'CNP', ['TpEntryMode','CdModoEntradaAutorizacao', 'NmMotivoAutorizacaoNegada', 'TipoImpacto']].dropna()
    # Adicionar as linhas ao conjunto de resultados
    for _, row in chunk_filtrado.iterrows():
        # Adicionar ao conjunto garantindo unicidade da coluna MotivoAutorizacaoNegada
        if (row['NmMotivoAutorizacaoNegada'],row['CdModoEntradaAutorizacao']) not in valores_trxs:
            valores_trxs.add((row['NmMotivoAutorizacaoNegada'], row['CdModoEntradaAutorizacao']))
            resultados.append(row)


# %%
# Criar DataFrame a partir do conjunto de resultados
df_resultados_trxs = pd.DataFrame(resultados)

# %%
df_resultados_trxs['CdModoEntradaAutorizacao'] = df_resultados_trxs['CdModoEntradaAutorizacao'].astype(str)

# %%
df_resultados_trxs['CdModoEntradaAutorizacao'] = df_resultados_trxs['CdModoEntradaAutorizacao'].str.replace('.0', '', regex=False)

# %%
df_resultados_trxs

# %%

df_resultados_trxs.to_csv(r"N:\DRSC\GRCF\GRF\Resultados Analise CNP\resultados_unicos_trxs_v3.csv", index=False, encoding='utf-8')
 
print("Resultados únicos salvos no arquivo: resultados_trxs_unicos.csv")

# %%
print(df_resultados_trxs['NmMotivoAutorizacaoNegada'].unique()).value_counts()

# %%
valores_unicos_combinados = df_resultados_trxs[['CdModoEntradaAutorizacao', 'NmMotivoAutorizacaoNegada', 'TipoImpacto']].drop_duplicates()
print("Combinações únicas de valores:")
valores_unicos_combinados

# %%
for coluna in df_resultados_trxs:
    valores_unicos_2= df_resultados_trxs[coluna].unique()
    print(f'{coluna} {valores_unicos_2}')


 
