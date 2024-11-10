from tkinter import *

width = 400
height = 300

def abreLogin():
    returnValue = -1

    def login():
        nonlocal returnValue
        usuario = Nome.get()
        senha = Senha.get()
        print(f"Usuário: {usuario}, Senha: {senha}")  # 
        returnValue = 1
        window.quit()
        window.destroy()

    def sair():
        nonlocal returnValue
        window.quit()
        window.destroy()
        returnValue = 0

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

    window.mainloop()
    
    return returnValue
