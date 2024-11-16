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

    def on_entry_click(event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')

    def on_focusout(event, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg = 'grey')

    # Configura a janela principal.
    window = Tk()
    window.title("Login")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")

    # Adiciona o ícone de usuário
    user_icon = Label(window, text="👤", font=("Arial", 40), bg="#2C3E50", fg="#ECF0F1")
    user_icon.pack(pady=10)

    # Texto de Login
    Label(window, text="LOGIN F1", font=("Arial", 16), bg="#2C3E50", fg="#ECF0F1").pack(pady=10)

    # Cria o campo de Usuário com placeholder
    Nome = Entry(window, width=30, font=("Arial", 12), fg='grey')
    Nome.insert(0, 'Usuário')
    Nome.bind('<FocusIn>', lambda event: on_entry_click(event, Nome, 'Usuário'))
    Nome.bind('<FocusOut>', lambda event: on_focusout(event, Nome, 'Usuário'))
    Nome.pack(pady=5)

    # Cria o campo de Senha com placeholder
    Senha = Entry(window, width=30, font=("Arial", 12), show="*", fg='grey')
    Senha.insert(0, 'Password')
    Senha.bind('<FocusIn>', lambda event: on_entry_click(event, Senha, 'Password'))
    Senha.bind('<FocusOut>', lambda event: on_focusout(event, Senha, 'Password'))
    Senha.pack(pady=5)

    # Cria o botão para Login.
    fButtons = Frame(window, bg="#2C3E50")
    fButtons.pack(pady=20)

    bLogin = Button(fButtons, text="Login", command=login, bg="#3498DB", fg="white", width=10, font=("Arial", 12), relief=GROOVE)
    bLogin.grid(row=0, column=0, padx=10)
    bSair = Button(fButtons, text="Sair", command=sair, width=10, font=("Arial", 12), relief=GROOVE)
    bSair.grid(row=0, column=1, padx=10)

    window.protocol("WM_DELETE_WINDOW", sair)
    window.mainloop()
    return [returnValue, userid]