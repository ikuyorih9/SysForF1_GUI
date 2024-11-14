from tkinter import *
from tkinter import ttk, messagebox
from sources import user
from PIL import Image, ImageTk

width = 1000
height = 600

def abreOverviewPiloto(connection, window, usuario):
    if usuario is None:
        return -1

    nome = "unknown"
    ano = -1
    tipo = ""
    idoriginal = ""
    cursor = connection.cursor()

    # Pega uma (e única) tupla da resposta.
    idoriginal = usuario.idoriginal

    if idoriginal:
        cursor.execute("SELECT forename || ' ' || surname FROM Driver WHERE driverid = %s;", (idoriginal,))
        nome = cursor.fetchone()[0]

        cursor.execute("""
            SELECT DISTINCT Constructors.name, Races.year 
            FROM Results, Constructors, Races 
            WHERE Results.driverid = %s AND 
                Results.constructorid = Constructors.constructorid AND 
                Results.raceid = Races.raceid ORDER BY Races.year DESC LIMIT 1;
        """, (idoriginal,))
        resultado = cursor.fetchone()
        escuderia, ano = resultado

        cursor.execute("""
            SELECT MIN(Races.year) AS primeiro_ano, MAX(Races.year) AS ultimo_ano
            FROM Results 
                JOIN Constructors ON Results.constructorid = Constructors.constructorid
                JOIN Races ON Results.raceid = Races.raceid
            WHERE Results.driverid = %s;
        """, (idoriginal,))
        primeiroano, ultimoano = cursor.fetchone()

    resultado2 = cursor.fetchall()


    # Configura estilos
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 12), background="#2C3E50", foreground="#ECF0F1")
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#2C3E50", foreground="#ECF0F1")

    # Título
    title_label = ttk.Label(window, text="Informações do Piloto", style="Title.TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Adiciona labels de informações
    ttk.Label(window, text="Usuário:", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=usuario.login, style="TLabel").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Nome:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=nome, style="TLabel").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Escuderia:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=f"{escuderia} ({ano})", style="TLabel").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Atividade:", style="TLabel").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=str(primeiroano) + " - " + str(ultimoano), style="TLabel").grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Centraliza as colunas
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

def abreOverviewEscuderia(connection, window, usuario):
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM Constructors WHERE constructorid = %s;", (usuario.idoriginal,))
    nome = cursor.fetchone()[0]

    
    cursor.execute("""
        SELECT COUNT(*)
        FROM RESULTS
        WHERE constructorid = %s AND rank = 1;
    """, (usuario.idoriginal,))

    qtdCorridasGanhas = cursor.fetchone()[0]

    # cursor.execute("""
    #     SELECT constructorid, COUNT(DISTINCT driverid)
    #     FROM RESULTS, RACES
    #     WHERE Races.raceid = Results.raceid AND
    #           Results.constructorid = %s AND
    #           (driverid, year) IN (
    #               SELECT DISTINCT driverid, MAX(year)
    #               FROM RESULTS, RACES
    #               WHERE Races.raceid = Results.raceid
    #               GROUP BY (driverid)
    #               ORDER BY driverid
    #           )
    #     GROUP BY constructorid
    #     ORDER BY constructorid;
    # """, (usuario.idoriginal,))

    cursor.execute("""
        SELECT constructorid, COUNT(DISTINCT driverid)
        FROM RESULTS
        WHERE constructorid = %s
        GROUP BY constructorid
        ORDER BY constructorid;
    """, (usuario.idoriginal,))

    qtdPilotos = cursor.fetchone()[1]

    cursor.execute("""
        SELECT MIN(year), MAX(year)
        FROM RESULTS
        JOIN RACES ON RESULTS.raceid = RACES.raceid
        WHERE RESULTS.constructorid = %s;
    """, (usuario.idoriginal,))
    primeiroAno, ultimoAno = cursor.fetchone()

    # Configura estilos
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 12), background="#2C3E50", foreground="#ECF0F1")
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#2C3E50", foreground="#ECF0F1")

    # Título
    title_label = ttk.Label(window, text="Informações da Escuderia", style="Title.TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Adiciona labels de informações
    ttk.Label(window, text="Usuário:", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=usuario.login, style="TLabel").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Nome:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=nome, style="TLabel").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Vitórias:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=str(qtdCorridasGanhas), style="TLabel").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Pilotos da Escuderia:", style="TLabel").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=str(qtdPilotos), style="TLabel").grid(row=4, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Atividade:", style="TLabel").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=str(primeiroAno) + " - " + str(ultimoAno), style="TLabel").grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Centraliza as colunas
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

def abreOverviewAdministrador(connection, window, usuario):

    mainFrame = Frame(window).grid(sticky="nsew")

    cursor = connection.cursor()

    imagem_original = Image.open("./images/key.png")
    imagem_redimensionada = imagem_original.resize((12, 12))
    imagem = ImageTk.PhotoImage(imagem_redimensionada)  
      
    headerFrame = Frame(mainFrame)
    headerFrame.grid(row=0, columnspan=4,padx=5, pady=5, sticky="nsew")

    # Label para o nome de usuário.
    Label(headerFrame, text="Usuário: " + usuario.login + " ", image=imagem, compound="right").grid(row=0, column=0, padx=5, sticky="w")

    Button(headerFrame, text="Cadastrar Piloto", command=lambda: print("Cadastrar Piloto!")).grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
    Button(headerFrame, text="Cadastrar escuderia", command=lambda: print("Cadastrar escuderia!")).grid(row=1, column=1, padx=15, pady=5, sticky="nsew")


    cursor.execute("""
        SELECT COUNT(DISTINCT driverid)
        FROM Driver;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdPilotos = resultado[0]

    # Label para a quantidade total de pilotos
    Label(mainFrame, text = "Quantidade de pilotos: " + str(qtdPilotos)).grid(row = 1, column = 0, padx=5, pady=5, sticky="w")
    
    # SEÇÃO DE ESCUDERIA

    cursor.execute("""
        SELECT COUNT(DISTINCT constructorid)
        FROM Constructors;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdEscuderias = resultado[0]

    # Label para a quantidade total de escuderias


    escuderiasFrame = Frame(mainFrame)
    escuderiasFrame.grid(row = 2, column = 0, padx=5, pady=5)

    Label(escuderiasFrame, text = "Quantidade de escuderias: " + str(qtdEscuderias)).grid(row = 0, column = 0, pady=5, sticky="w")

    escuderiaTabela = ttk.Treeview(escuderiasFrame, columns=("Escuderia", "Pilotos"), show="headings")
    escuderiaTabela.heading("Escuderia", text="Escuderia")
    escuderiaTabela.heading("Pilotos", text="Qtd. Pilotos")

    cursor.execute("""
        SELECT Constructors.constructorid, Constructors.name, COUNT(DISTINCT driverid)
        FROM RESULTS, RACES, Constructors
        WHERE Races.raceid = Results.raceid AND
              Results.constructorid = Constructors.constructorid AND 
              (driverid, year) IN (
                    SELECT DISTINCT driverid, MAX(year)
                    FROM RESULTS, RACES
                    WHERE Races.raceid = Results.raceid
                    GROUP BY (driverid)
                    ORDER BY driverid
            )
        GROUP BY (Constructors.constructorid, Constructors.name)
        ORDER BY constructorid;
    """)
    escuderias = cursor.fetchall()

    if escuderias:
        for tupla in escuderias:
            id, nome, qtdPilotos = tupla
            escuderiaTabela.insert("", "end", values=(nome, qtdPilotos))
    
    escuderiaTabela.grid(row = 1)

    
    # SEÇÃO DE CIRCUITOS

    cursor.execute("""
        SELECT COUNT(DISTINCT raceid)
        FROM RACES;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdCircuitos = resultado[0]

    # Label para a quantidade total de escuderias

    circuitosFrame = Frame(mainFrame)
    circuitosFrame.grid(row = 2, column = 1, padx=5, pady=5)

    Label(circuitosFrame, text = "Quantidade de circuitos: " + str(qtdCircuitos)).grid(row = 0, column = 0, pady=5, sticky="w")

    circuitosTabela = ttk.Treeview(circuitosFrame, columns=("Circuito", "Corridas"), show="headings")
    circuitosTabela.heading("Circuito", text="Circuito")
    circuitosTabela.heading("Corridas", text="Qtd. Corridas")

    cursor.execute("""
        SELECT Circuits.circuitid, Circuits.name, COUNT(DISTINCT raceid)
        FROM RACES LEFT JOIN CIRCUITS ON Races.circuitid = Circuits.circuitid
        GROUP BY (Circuits.circuitid, Circuits.name)
        ORDER BY Circuits.circuitid
    """)
    resultado = cursor.fetchall()
    if resultado:
        for tupla in resultado:
            id, nome, qtd = tupla
            circuitosTabela.insert("", "end", values=(nome, qtd))

    circuitosTabela.grid(row = 1)


    # SEÇÃO DE TEMPORADA

    seasonFrame = Frame(mainFrame)
    seasonFrame.grid(row = 4, columnspan=2, padx=5, pady=5)

    seasonTabela = ttk.Treeview(seasonFrame, columns=("Temporada", "Corridas"), show="headings")
    seasonTabela.heading("Temporada", text="Circuito")
    seasonTabela.heading("Corridas", text="Qtd. Corridas")

    cursor.execute("""
        SELECT Seasons.year, COUNT(DISTINCT Races.raceid)
        FROM Races LEFT JOIN Seasons ON Races.year = Seasons.year
        GROUP BY Seasons.year
        ORDER BY Seasons.year ASC;
    """)
    resultado = cursor.fetchall()

    if resultado:
        for tupla in resultado:
            ano, qtd = tupla
            seasonTabela.insert("", "end", values=(ano, qtd))

    seasonTabela.grid(row = 0)

    window.mainloop()


def abreOverview(connection, usuario):
    # Configura a janela principal.
    window = Tk()
    window.title("Overview")
    window.geometry(f"{width}x{height}")
    window.resizable(True, True)
    window.configure(bg="#2C3E50")

    # Função para carregar as informações conforme o tipo do usuário
    if usuario.tipo == 'Piloto':
        abreOverviewPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreOverviewEscuderia(connection, window, usuario)
    elif usuario.tipo == 'Administrador':
        abreOverviewAdministrador(connection, window, usuario)

    window.mainloop()
