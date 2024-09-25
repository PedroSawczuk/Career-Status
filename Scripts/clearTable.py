import mysql.connector

dbConfig = {
    'user': 'root',
    'password': 'alunoifro',
    'host': 'localhost',
    'port': '3306',
    'database': 'careerstatus_db'
}

tabelas = [
    'app_estatistica',
    'app_jogador',
    'app_nacionalidadeestatistica'
]

try:
    connection = mysql.connector.connect(**dbConfig)
    cursor = connection.cursor()

    for table in tabelas:
        cursor.execute(f"DELETE FROM {table};")
        print(f"Registros deletados da tabela {table}")

    connection.commit()

except mysql.connector.Error as err:
    print(f"Erro: {err}")
    if connection:
        connection.rollback()
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("Limpeza das tabelas concluída.")
