import mysql.connector
from mysql.connector import Error

def create_database(host, user, password, name, port=3306):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE {}".format(name))
        print("Database {} criado com sucesso!".format(name))
    except Error as e:
        print("Erro ao criar o banco de dados:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão ao MySQL encerrada.")

def main():
    name = input("Nome do banco de dados: ")
    user = input("Usuário do banco de dados: ")
    password = input("Senha do banco de dados: ")
    host = input("Host do banco de dados (pressione Enter para padrão localhost): ")
    port = input("Porta do banco de dados (pressione Enter para padrão 3306): ")

    if not host:
        host = "localhost"
    if not port:
        port = 3306
    else:
        port = int(port)

    create_database(host, user, password, name, port)

if __name__ == "__main__":
    main()
