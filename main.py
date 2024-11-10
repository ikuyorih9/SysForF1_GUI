from sources import login
import psycopg2
import configparser

usuario = ""

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

    proximaJanela, usuario = login.abreLogin(connection)
    print(proximaJanela)
    print(usuario)
    
    if proximaJanela == 0:
        print("Fechar janela!")
        


except Exception as error:
    print("Erro ao conectar com o postgreSQL:", error)