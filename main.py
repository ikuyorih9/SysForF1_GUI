from sources import login
import psycopg2
import configparser


#print(login.abreLogin())

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
    nextstep = login.abreLogin(connection)

except Exception as error:
    print("Erro ao conectar com o postgreSQL:", error)