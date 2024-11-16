from tkinter import *
from tkinter import messagebox
from sources import user
from sources.layouts import *
from sources.navigation import *
from tkcalendar import DateEntry
import psycopg2

width = 600
height = 400

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
    def insereBase():
        cursor = connection.cursor()
        cursor.execute("""
            SELECT driverid+1
            FROM Driver
            ORDER BY driverid DESC
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        if resultado:
            id = resultado[0]
        ref = eRef.get()
        number = int(enumero.get())
        code = int(ecode.get())
        pnome = eforename.get()
        unome = esurname.get()
        nasc = enasc.get_date()
        nacionalidade = enationality.get()
        url = eurl.get()

        try:
            cursor.execute("INSERT INTO Driver(driverid, driverref, number, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, ref, number, code, pnome, unome, nasc, nacionalidade, url))
            connection.commit()
            messagebox.showinfo("Inserido com sucesso",f"Novo piloto {pnome} {unome} ({id}) foi inserido na base de dados!")

        except psycopg2.errors.UniqueViolation as e:
            messagebox.showerror("Violação de regra",f"Já há um piloto referenciada por {ref}")
        except psycopg2.errors.InFailedSqlTransaction as e:
            messagebox.showerror("Falha na transação",f"Piloto não foi inserido na base de dados.")

    window.title("Cadastrar piloto")

    fWindow = Frame(window, bg="#2C3E50")
    fWindow.pack(fill="both", expand=True)

    lHeader = cria_label(fWindow, "Cadastro de Pilotos", 24, "bold")
    lHeader.pack(padx=10,pady=10)

    fForm = Frame(fWindow, bg="#2C3E50")
    fForm.pack(padx=10,pady=5)

    lRef = cria_label(fForm, "DriverRef:", 12, "normal")
    lRef.grid(row=0, column=0, pady=5, sticky = "w")
    eRef = cria_entry(fForm, "Insira o driverRef", 10)
    eRef.grid(row=0, column=1, padx=5, pady=5)

    lnumero = cria_label(fForm, "Número:", 12, "normal")
    lnumero.grid(row=1, column=0, pady=5, sticky = "w")
    enumero = cria_entry(fForm, "Insira o número", 10)
    enumero.grid(row=1,column=1, padx=5, pady=5)

    lcode = cria_label(fForm, "Código:", 12, "normal")
    lcode.grid(row=2, column=0, pady=5, sticky = "w")
    ecode = cria_entry(fForm, "Insira o código", 10)
    ecode.grid(row=2,column=1, padx=5, pady=5)

    lforename = cria_label(fForm, "Primeiro nome:", 12, "normal")
    lforename.grid(row=3, column=0, pady=5, sticky = "w")
    eforename = cria_entry(fForm, "Insira o primeiro nome", 10)
    eforename.grid(row=3,column=1, padx=5, pady=5)

    lsurname = cria_label(fForm, "Sobrenome:", 12, "normal")
    lsurname.grid(row=4, column=0, pady=5, sticky = "w")
    esurname = cria_entry(fForm, "Insira o sobrenome", 10)
    esurname.grid(row=4,column=1, padx=5, pady=5)

    lnasc = cria_label(fForm, "Nascimento:", 12, "normal")
    lnasc.grid(row=5, column=0, pady=5, sticky = "w")
    enasc = DateEntry(fForm, borderwidth=2, date_pattern='dd/mm/yyyy')
    enasc.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

    lnationality = cria_label(fForm, "Nacionalidade:", 12, "normal")
    lnationality.grid(row=6, column=0, pady=5, sticky = "w")
    enationality = cria_entry(fForm, "Insira a nacionalidade", 10)
    enationality.grid(row=6, column=1, padx=5, pady=5)

    lurl = cria_label(fForm, "URL:", 12, "normal")
    lurl.grid(row=7, column=0, pady=5, sticky = "w")
    eurl = cria_entry(fForm, "Insira a URL", 10)
    eurl.grid(row=7,column=1, padx=5, pady=5)

    fButton = Frame(fWindow, bg="#2C3E50")
    fButton.pack(pady=10)

    bVoltar = cria_botao(fButton, "Sair", 12, lambda: go_back(window))
    bVoltar.pack(padx=20, side="left")
    bCadastrar = cria_botao(fButton, "Cadastrar", 12, insereBase)
    bCadastrar.pack(padx=20, side="left")

    window.protocol("WM_DELETE_WINDOW", lambda:go_back(window))
    window.mainloop()


def cadastroEscuderia(connection, window):
    def insereBase():
        cursor = connection.cursor()
        cursor.execute("""
            SELECT constructorid+1
            FROM Constructors
            ORDER BY constructorid DESC
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        if resultado:
            id = resultado[0]
        ref = eRef.get()
        nome = enome.get()
        nacionalidade = enationality.get()
        url = eurl.get()

        try:
            cursor.execute("INSERT INTO Constructors(constructorid, constructorref, name, nationality, url) VALUES (%s, %s, %s, %s, %s)", (id, ref, nome, nacionalidade, url))
            connection.commit()
            messagebox.showinfo("Inserido com sucesso",f"Nova escuderia {nome} ({id}) foi inserido na base de dados!")

        except psycopg2.errors.UniqueViolation as e:
            messagebox.showerror("Violação de regra",f"Já há uma escuderia referenciada por {ref}")
        except psycopg2.errors.InFailedSqlTransaction as e:
            messagebox.showerror("Falha na transação",f"Escuderia não foi inserida na base de dados.")

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
    bCadastrar = Button(buttonFrame, text="Cadastrar", command = insereBase) 
    bCadastrar.pack(padx=20, side="left")

    window.protocol("WM_DELETE_WINDOW", lambda:go_back(window))
    window.mainloop()