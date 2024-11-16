import psycopg2

class Usuario:
    def __init__(self, userid, login, senha, tipo, idoriginal):
        self.userid = userid
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.idoriginal = idoriginal

def imprimeUsuario(usuario):
    print("Imprimindo usuário...")
    print("\t-Userid: ", usuario.userid)
    print("\t-Login: ", usuario.login)
    print("\t-Senha: ", usuario.senha)
    print("\t-Tipo: ", usuario.tipo)
    print("\t-Idoriginal: ", usuario.idoriginal)

def carregaInfoUsuario(userid, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT userid, login, password, tipo, idoriginal FROM Users WHERE userid = %s;", (userid,))
    user = cursor.fetchone()
    print(user)
    if user:
        return Usuario(user[0], user[1], user[2], user[3], user[4])
    return None