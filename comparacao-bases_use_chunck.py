#Analisando duas bases de dados csv para verificar incosistencias de codigos de solicitação autorizacao
# %%
import pandas as pd
 
# %%
consulta= r"C:\Users\actct.asilmara\OneDrive - Banco Votorantim S.A\Documentos\Autorizacao cartoes\consulta.csv"
consulta_erica= r"N:\DRSC\GRCF\GRF\BASE_COD_ERICA.csv"
 
# %%
coluna_comparacao= 'MotivoAutorizacaoNegada'
 
# %%
valores_consulta= set()
valores_consulta_erica= set()
 
# %%
chunksize=100_000
for chunk in pd.read_csv(r"C:\Users\actct.asilmara\OneDrive - Banco Votorantim S.A\Documentos\Autorizacao cartoes\consulta.csv", sep=';', encoding='utf-8,', chunksize=chunksize):
    valores_consulta.update(chunk['MotivoAutorizacaoNegada'].dropna().unique())
 
# %%
chunksize=100_000
for chunk in pd.read_csv(r"N:\DRSC\GRCF\GRF\BASE_COD_ERICA.csv", sep=';', encoding='utf-8,', chunksize=chunksize):
    valores_consulta_erica.update(chunk['MotivoAutorizacaoNegada'].dropna().unique())
 
# %%
# Comparar os valores
diferencas_base1_nao_base2 = valores_consulta - valores_consulta_erica
diferencas_base2_nao_base1 = valores_consulta_erica - valores_consulta
 
# %%
print(f"Valores na Base 1 que não estão na Base 2: {len(diferencas_base1_nao_base2)}")
#print(diferencas_base1_nao_base2)
 
for i, v in enumerate (diferencas_base1_nao_base2):
    print(i, v)
 
# %%
print(f"Valores na Base 2 que não estão na Base 1: {len(diferencas_base2_nao_base1)}")
print(diferencas_base2_nao_base1)
 
 
 
 
 
 
