from tkinter import *
from sources import user
from sources.navigation import *

width = 1000
height = 600

def cadastrar(connection, tipoCadastro):
    # Configura a janela principal.
    window = Toplevel()
    window.title("Cadastro")
    window.geometry(f"{width}x{height}")
    window.resizable(True, True)

    if tipoCadastro == 1:
        cadastroPiloto(connection, window)
    elif tipoCadastro == 2:
        cadastroEscuderia(connection, window)
    else:
        print("ERRO: cadastro recebe parâmetro inválido")
        exit()


def cadastroPiloto(connection, window):
    window.title("Cadastrar piloto")
    window.mainloop()

def desabilitar(window):
    for child in window.winfo_children():
        child.configure(state='disable')


def cadastroEscuderia(connection, window):
    window.title("Cadastrar escuderia")

    windowFrame = Frame(window, bg="#2C3E50")
    windowFrame.pack(fill="both", expand=True)

    lHeader = Label(windowFrame, text="Cadastro de Escuderia", font=("Montserrat", 24, "bold"))
    lHeader.pack(padx=10,pady=10)

    formFrame = Frame(windowFrame, bg="#2C3E50")
    formFrame.pack(padx=10,pady=5)

    lRef = Label(formFrame, text="ConstructorRef: ")
    lRef.grid(row=0, column=0, pady=5, sticky = "w")
    eRef = Entry(formFrame)
    eRef.grid(row=0, column=1, padx=5, pady=5)

    lnome = Label(formFrame, text="Nome: ")
    lnome.grid(row=1, column=0, pady=5, sticky = "w")
    enome = Entry(formFrame)
    enome.grid(row=1,column=1, padx=5, pady=5)

    lnationality = Label(formFrame, text="Nacionalidade: ")
    lnationality.grid(row=2, column=0, pady=5, sticky = "w")
    enationality = Entry(formFrame)
    enationality.grid(row=2, column=1, padx=5, pady=5)

    lurl = Label(formFrame, text="URL: ")
    lurl.grid(row=3, column=0, pady=5, sticky = "w")
    eurl = Entry(formFrame)
    eurl.grid(row=3,column=1, padx=5, pady=5)

    buttonFrame = Frame(windowFrame, bg="#2C3E50")
    buttonFrame.pack(pady=10)

    bVoltar = Button(buttonFrame, text="Voltar", command = lambda: go_back(window)) 
    bVoltar.pack(padx=20, side="left")
    bCadastrar = Button(buttonFrame, text="Cadastrar", command = lambda:print("Cadastrar")) 
    bCadastrar.pack(padx=20, side="left")

    window.protocol("WM_DELETE_WINDOW", lambda:go_back(window))
    window.mainloop()