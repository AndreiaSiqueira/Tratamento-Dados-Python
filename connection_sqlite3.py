#Criando conexao com sqlite3, create, into, update dados na base
# %%

import sqlite3


# %%

# Cria (ou conecta a) um banco de dados chamado 'meu_banco.db'
conexao = sqlite3.connect('db_cadastro.db')


# %%

# Cria um cursor para executar comandos SQL
cursor = conexao.cursor()


# %%


# Cria uma tabela de exemplo
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
id INTEGER PRIMARY KEY,
nome TEXT NOT NULL,
email TEXT UNIQUE NOT NULL
    )""")

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()





# %%
conexao = sqlite3.connect('db_cadastro.db')

cursor = conexao.cursor()


# %%

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas no banco de dados:")

for tabela in tabelas:
    print(tabela[0])



# %%
cursor.execute("PRAGMA table_info(usuarios);")
colunas = cursor.fetchall()

for coluna in colunas:
    print(coluna)


# %%

cursor.execute("DROP TABLE IF EXISTS usuarios")
conexao.commit()


# %%
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
id INTEGER PRIMARY KEY,
nome TEXT NOT NULL,
email TEXT UNIQUE NOT NULL
    )""")

# Salva as alterações e fecha a conexão
conexao.commit()

# %%
cursor.execute("PRAGMA table_info(usuarios);")
colunas = cursor.fetchall()
for coluna in colunas:
    print(coluna)

# %%

cursor.execute("""
INSERT INTO usuarios (nome, email)
VALUES (?, ?)
""", ("João Silva", "joao@email.com"))


# %%
cursor.execute("SELECT * FROM usuarios")
usuarios= cursor.fetchall()
for usuario in usuarios:
    print(usuario)


 
