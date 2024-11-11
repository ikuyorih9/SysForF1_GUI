from sources import login
from sources import overview
from sources import user
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
        port = config['postgresql']['port']
    )

    proximaJanela, userid = login.abreLogin(connection)
    usuario = user.carregaInfoUsuario(userid, connection)
    
    if(proximaJanela == 1):
        overview.abreOverview(connection, usuario)
    elif proximaJanela == 0:
        print("Fechar janela!")

except psycopg2.OperationalError as error:
    print("Erro de conexão:", error)

except tkinter.TclError as error:
    print("NOT_FOUND_IMAGE: ", error)



finally:
    # Garante que a conexão será fechada, se foi estabelecida
    if 'connection' in locals() and connection is not None:
        connection.close()
        print("Conexão fechada com sucesso.")