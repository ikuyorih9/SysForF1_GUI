from sources import navigation
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import hashlib

width = 400
height = 300

def abreLogin(connection):
    returnValue = -1
    userid = -1
    cursor = connection.cursor()

    def registraLogin(userid):
        data = datetime.now()
        print(data)
        cursor.execute("INSERT INTO Log_Table(userid, data) VALUES (%s,%s);", (userid, data))
        connection.commit()

    def login():
        nonlocal returnValue
        nonlocal userid

        usuario = Nome.get()
        senha = hashlib.md5(Senha.get().encode()).hexdigest()
        
        cursor.execute("SELECT userid FROM Users WHERE login = %s AND password = %s;", (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            userid = resultado
            registraLogin(userid)
            returnValue = 1
            navigation.push(window)
            window.withdraw()
            window.quit()
            return
        else:
            print("NOT_FOUND_DB: usuario nao foi encontrado na base.")

        messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")

    def sair():
        nonlocal returnValue
        window.destroy()
        returnValue = 0

    def aaa():
        mywindow = Toplevel()
        mywindow.title("Overview")
        mywindow.geometry(f"{width}x{height}")
        mywindow.resizable(True, True)
        Label(mywindow, text="AAA").grid(row=0, column=0, padx=5, sticky="w")
        window.withdraw()
        mywindow.mainloop()

    # Configura a janela principal.
    window = Tk()
    window.title("Login")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)

    # Texto de Login
    Label(window, text="LOGIN F1", font=("Lucida Grande", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Cria o campo de Usuário
    Label(window, text="Usuário", width=10).grid(row=1, column=0, padx=0, pady = 5, sticky="w")
    Nome = Entry(window, width=50)
    Nome.grid(row=1, column=1, padx=0, pady=5)

    # Cria o campo de Senha
    Label(window, text="Senha", width=10).grid(row=2, column=0, padx=0, pady = 5, sticky="w")
    Senha = Entry(window, show="*", width=50)
    Senha.grid(row=2, column=1, padx=0, pady=5)

    # Cria o botão para Login.
    fButtons = Frame(window)
    fButtons.grid(row=3, column=0, columnspan=2, pady=20)

    bLogin = Button(fButtons, text="Sign in", command = login) 
    bLogin.grid(row=3, column=0, sticky="e")
    bSair = Button(fButtons, text="Sair", command = sair) 
    bSair.grid(row=3, column=1, padx=10, sticky="w")

    myb = Button(fButtons, text="aaa", command = aaa) 
    myb.grid(row=4, column=0, sticky="e")

    window.protocol("WM_DELETE_WINDOW", sair)
    window.mainloop()
    return [returnValue, userid]
