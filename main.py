from sources import login
from sources import overview
from sources import user
from sources import navigation
import psycopg2
import tkinter
import configparser

try:
    # ESTABELECE A CONEXÃO COM A BASE DE DADOS
    config = configparser.ConfigParser()
    config.read('database.ini')

    # Verifica se a seção 'postgresql' foi lida corretamente
    if 'postgresql' not in config:
        raise Exception("Erro: Seção 'postgresql' não encontrada no arquivo de configuração.")

    connection = psycopg2.connect(
        dbname = config['postgresql']['dbname'],
        user = config['postgresql']['user'],
        password = config['postgresql']['password'],
        host = config['postgresql']['host'],
        port = config['postgresql']['port'],
        connect_timeout=int(config['postgresql']['timeout_conn'])
    )

    login.abreLogin(connection)

#Exceções(erro de conexao, imagem nao encontrada)
except psycopg2.OperationalError as error:
    print("CONNECTION_ERROR:", error)


finally:
    # Garante que a conexão será fechada, se foi estabelecida
    if 'connection' in locals() and connection is not None:
        connection.close()
        print("Conexão fechada com sucesso.")