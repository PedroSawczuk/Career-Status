import mysql.connector

# Configurações do banco de dados
db_config = {
    'user': 'root',
    'password': 'alunoifro',
    'host': 'localhost',
    'port': '3306',
    'database': 'careerstatus_db'
}

# Tabelas a serem limpas
tables = [
    'app_estatistica',
    'app_jogador',
    'app_nacionalidadeestatistica'
]

try:
    # Conectando ao banco de dados
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Limpando cada tabela
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        print(f"Registros deletados da tabela {table}")

    # Confirmando as alterações
    connection.commit()

except mysql.connector.Error as err:
    print(f"Erro: {err}")
    if connection:
        connection.rollback()
finally:
    # Fechando a conexão com o banco de dados
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("Limpeza das tabelas concluída.")
