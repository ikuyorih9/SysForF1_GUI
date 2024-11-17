from sources import navigation
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from sources.layouts import *
from sources.navigation import * 
from sources.user import *
from sources.overview import *
import hashlib
from PIL import Image, ImageTk

width = 400
height = 300

def abreLogin(connection):
    def login():
        usuario = lNome.get()
        senha = hashlib.md5(lSenha.get().encode()).hexdigest()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE login = %s AND password = %s;", (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            # Obtém o userid da busca.
            usuario = Usuario(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])

            # Salva o log de login
            data = datetime.now()
            cursor.execute("INSERT INTO Log_Table(userid, data) VALUES (%s,%s);", (usuario.userid, data))
            connection.commit()

            go_forward(window, lambda:abreOverview(connection, usuario))
            return
        else:
            print("NOT_FOUND_DB: usuario nao foi encontrado na base.")

        messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")

    # Configura a janela principal.
    window = Tk()
    window.title("Login")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda:close_all_windows(window))
    
    # Adiciona o evento para pressionar Enter
    window.bind('<Return>', lambda event: login())

    # Adiciona o evento para pressionar Esc
    window.bind('<Escape>', lambda event: close_all_windows(window))

    fLogin = Frame(window, bg="#2C3E50")
    fLogin.pack(fill="both", expand=True)

    # Abre imagem no ícone de usuário
    img = Image.open("./images/user.png")
    img = img.resize((60, 60), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    # Adiciona o ícone de usuário
    user_icon = cria_label_image(fLogin, image=photo)
    user_icon.pack(pady=10)

    # Texto de Login
    cria_label(fLogin, "LOGIN", fontsize=16).pack(pady=10)

    # Cria o campo de Usuário com placeholder
    lNome = cria_entry(fLogin, 'Usuário',  width=30)
    lNome.pack(pady=5)

    # Cria o campo de Senha com placeholder
    lSenha = cria_entry(fLogin, 'Password', width=30, show="*")
    lSenha.pack(pady=5)

    # Cria o botão para Login.
    fButtons = Frame(fLogin, bg="#2C3E50")
    fButtons.pack(pady=20)
 
    bLogin = cria_botao(fButtons, "Login", command = login)
    bLogin.grid(row=0, column=0, padx=10)
    bSair = cria_botao(fButtons, "Sair", command = lambda:close_all_windows(window))
    bSair.grid(row=0, column=1, padx=10)

    
    window.mainloop()
