from sources import navigation
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from sources.layouts import *
import hashlib
from PIL import Image, ImageTk

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

    # Configura a janela principal.
    window = Tk()
    window.title("Login")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")

    # Configura estilos
    titleTextSize = 16
    titleTextStyle = "bold"
    labelTextSize = 12
    labelTextStyle = "normal"
    entryWidth = 30

    # Abre imagem no ícone de usuário
    img = Image.open("./images/user.png")
    img = img.resize((60, 60), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    # Adiciona o ícone de usuário
    user_icon = Label(window, image=photo, bg="#2C3E50")
    user_icon.pack(pady=10)

    # Texto de Login
    cria_label(window, "LOGIN F1", titleTextSize, titleTextStyle).pack(pady=10)

    # Cria o campo de Usuário com placeholder
    Nome = cria_entry(window, 'Usuário', labelTextSize, entryWidth)
    Nome.pack(pady=5)

    # Cria o campo de Senha com placeholder
    Senha = cria_entry(window, 'Password', labelTextSize, entryWidth, "*")
    Senha.pack(pady=5)

    # Adiciona o evento para pressionar Enter
    window.bind('<Return>', lambda event: login())

    # Adiciona o evento para pressionar Esc
    window.bind('<Escape>', lambda event: sair())

    # Cria o botão para Login.
    fButtons = Frame(window, bg="#2C3E50")
    fButtons.pack(pady=20)

    bLogin = cria_botao(fButtons, "Login", labelTextSize, login)
    bLogin.grid(row=0, column=0, padx=10)
    bSair = cria_botao(fButtons, "Sair", labelTextSize, sair)
    bSair.grid(row=0, column=1, padx=10)

    window.protocol("WM_DELETE_WINDOW", sair)
    window.mainloop()

    return [returnValue, userid]
