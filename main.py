from sources import login
from sources import overview
from sources import user
import psycopg2
import configparser

try:
    # ESTABELECE A CONEXÃO COM A BASE DE DADOS
    config = configparser.ConfigParser()
    config.read('database.ini')

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
    
    if proximaJanela == 0:
        print("Fechar janela!")

except psycopg2.OperationalError as error:
    print("Erro de conexão:", error)

except Exception as error:
    print("Erro generico:", error)
