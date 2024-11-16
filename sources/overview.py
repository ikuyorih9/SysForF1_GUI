from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import PhotoImage
from sources import user
from sources import cadastro
from sources import navigation
from sources.layouts import *
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


        cursor.execute("""
            SELECT Races.year, Circuits.name AS circuito, 
                        SUM(Results.points) AS total_pontos, 
                        SUM(CASE WHEN Results.position = 1 THEN 1 ELSE 0 END) AS total_vitorias
                    FROM Results
                    JOIN Races ON Results.raceid = Races.raceid
                    JOIN Circuits ON Races.circuitid = Circuits.circuitid
                    WHERE Results.driverid = 1
                    GROUP BY Races.year, Circuits.name
                    ORDER BY Races.year, Circuits.name;

        """, (idoriginal,))
        

    resultado2 = cursor.fetchall()


    # Configura estilos
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 12), background="#2C3E50", foreground="#ECF0F1")
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#2C3E50", foreground="#ECF0F1")

    # Título
    title_label = cria_label(window, text="Informações do Piloto", style="Title.TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Adiciona labels de informações
    cria_label(window, text="Usuário:", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=usuario.login, style="TLabel").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    cria_label(window, text="Nome:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=nome, style="TLabel").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    cria_label(window, text="Escuderia:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=f"{escuderia} ({ano})", style="TLabel").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    cria_label(window, text="Atividade:", style="TLabel").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=str(primeiroano) + " - " + str(ultimoano), style="TLabel").grid(row=4, column=1, padx=5, pady=5, sticky="w")
    
    pilotoFrame = Frame(window)
    pilotoFrame.grid(row = 5, column = 0, padx=5, pady=5)

   
    pilotoTabela = ttk.Treeview(pilotoFrame, columns=("Ano", "Circuito", "Total_Pontos", "Total_Vitorias"), show="headings")
    pilotoTabela.heading("Ano", text="Ano")
    pilotoTabela.heading("Circuito", text="Circuito")
    pilotoTabela.heading("Total_Pontos", text="Total de Pontos")
    pilotoTabela.heading("Total_Vitorias", text="Total de Vitorias")

    if resultado2:
       for tupla in resultado2:
            ano, circuito, total_pontos, total_vitorias = tupla
            pilotoTabela.insert("", "end", values=(ano, circuito, total_pontos, total_vitorias))

    pilotoTabela.grid(row = 5)

    # Centraliza as colunas
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1) 

def abreOverviewEscuderia(connection, window, usuario):

    cursor = connection.cursor()

    cursor.execute("SELECT name FROM Constructors WHERE constructorid = %s;", (usuario.idoriginal,))
    nome = cursor.fetchone()[0]

    cursor.execute("""
        SELECT constructorid, COUNT(DISTINCT driverid)
        FROM RESULTS, RACES
        WHERE Races.raceid = Results.raceid AND
              Results.constructorid = %s AND
              (driverid, year) IN (
                  SELECT DISTINCT driverid, MAX(year)
                  FROM RESULTS, RACES
                  WHERE Races.raceid = Results.raceid
                  GROUP BY (driverid)
                  ORDER BY driverid
              )
        GROUP BY constructorid
        ORDER BY constructorid;
    """, (usuario.idoriginal,))

    qtdPilotos = cursor.fetchone()[1]

    # Configura estilos
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 12), background="#2C3E50", foreground="#ECF0F1")
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#2C3E50", foreground="#ECF0F1")

    # Título
    title_label = cria_label(window, text="Informações da Escuderia", style="Title.TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Adiciona labels de informações
    cria_label(window, text="Usuário:", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=usuario.login, style="TLabel").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    cria_label(window, text="Nome:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=nome, style="TLabel").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    cria_label(window, text="Quantidade de pilotos:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    cria_label(window, text=str(qtdPilotos), style="TLabel").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Centraliza as colunas
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

def abreOverviewAdministrador(connection, overviewWindow, usuario):
    def sair():
        navigation.go_back(overviewWindow).destroy()

    cursor = connection.cursor()

    # BUSCAS (QUERIES)

    cursor.execute("""
        SELECT COUNT(DISTINCT driverid)
        FROM Driver;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdPilotos = resultado[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT constructorid)
        FROM Constructors;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdEscuderias = resultado[0]

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

    cursor.execute("""
        SELECT COUNT(DISTINCT raceid)
        FROM RACES;
    """)
    resultado = cursor.fetchone()
    if resultado:
        qtdCircuitos = resultado[0]

    cursor.execute("""
        SELECT Circuits.circuitid, Circuits.name, COUNT(DISTINCT raceid)
        FROM RACES LEFT JOIN CIRCUITS ON Races.circuitid = Circuits.circuitid
        GROUP BY (Circuits.circuitid, Circuits.name)
        ORDER BY Circuits.circuitid
    """)
    circuitos = cursor.fetchall()

    cursor.execute("""
        SELECT Seasons.year, COUNT(DISTINCT Races.raceid)
        FROM Races LEFT JOIN Seasons ON Races.year = Seasons.year
        GROUP BY Seasons.year
        ORDER BY Seasons.year ASC;
    """)
    temporadas = cursor.fetchall()

    mainFrame = cria_scrollable_frame(overviewWindow)

    # HEADER DO OVERVIEW
    # Cria um frame para conter o cabeçalho.
    fHeader = Frame(mainFrame, bg="#2C3E50")
    fHeader.pack(padx=10,pady=10)

    # Carrega uma imagem e redimensiona.
    imagem_original = Image.open("./images/key.png")
    imagem_redimensionada = imagem_original.resize((12, 12))
    imagem = ImageTk.PhotoImage(imagem_redimensionada)  

    # Cria label para o nome de usuário.
    cria_label_image(fHeader, "Usuário: " + usuario.login + " ", 14, "bold", imagem).grid(row=0, column=0, columnspan=2, padx=5, pady=10)

    # Cria botões de cadastro
    cria_botao(fHeader, "Cadastrar Piloto", 12, sair).grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
    cria_botao(fHeader, "Cadastrar Escuderia", 12, sair).grid(row=1, column=1, padx=15, pady=5, sticky="nsew")

    # Label para a quantidade total de pilotos, 
    cria_label(fHeader, "Quantidade de pilotos cadastrados: ", 12, "normal").grid(row = 2, column = 0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, str(qtdPilotos), 12, "normal").grid(row = 2, column = 1, padx=5, pady=5, sticky="e")

    # Label para a quantidade total de escuderias
    cria_label(fHeader, "Quantidade de escuderias cadastradas: ", 12, "normal").grid(row = 3, column = 0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, str(qtdEscuderias), 12, "normal").grid(row = 3, column = 1, padx=5, pady=5, sticky="e")

    # Label para a quantidade total de circuitos
    cria_label(fHeader, "Quantidade de circuitos cadastrados: ", 12, "normal").grid(row = 4, column = 0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, str(qtdCircuitos), 12, "normal").grid(row = 4, column = 1, padx=5, pady=5, sticky="e")

    # TABELA DE ESCUDERIAS
    # Cria um frame para conter a tabela de escuderias.
    fEscuderia = Frame(mainFrame, bg="#2C3E50")
    fEscuderia.pack(fill="x", pady=10)

    # Cria label de título para a tabela.
    cria_label(fEscuderia, "Quantidade de pilotos por escuderia", 12, "normal").pack(fill="x")

    # Cria a tabela de escuderias.
    escuderiaTabela = ttk.Treeview(fEscuderia, columns=("Escuderia", "Pilotos"), show="headings")
    escuderiaTabela.heading("Escuderia", text="Escuderia")
    escuderiaTabela.heading("Pilotos", text="Qtd. Pilotos")

    # Adiciona as escuderias na tabela
    if escuderias:
        for tupla in escuderias:
            id, nome, qtdPilotos = tupla
            escuderiaTabela.insert("", "end", values=(nome, qtdPilotos))
    
    escuderiaTabela.pack(padx = 10, pady = 5, fill="x")

    
    # TABELA DE CIRCUITOS
    # Cria um frame para a tabela de circuitos.
    fCircuitos = Frame(mainFrame, bg="#2C3E50")
    fCircuitos.pack(pady=10, fill="x")

    # Cria label de título para a tabela.
    cria_label(fCircuitos, "Quantidade de corridas por circuito", 12, "normal").pack(fill="x")

    # Cria a tabela de circuitos.
    circuitosTabela = ttk.Treeview(fCircuitos, columns=("Circuito", "Corridas"), show="headings")
    circuitosTabela.heading("Circuito", text="Circuito")
    circuitosTabela.heading("Corridas", text="Qtd. Corridas")

    if circuitos:
        for tupla in circuitos:
            id, nome, qtd = tupla
            circuitosTabela.insert("", "end", values=(nome, qtd))

    circuitosTabela.pack(padx = 10, pady = 5, fill="x")

    # TABELA DE TEMPORADA
    # Cria um frame para a tabela de temporada.
    fSeason = Frame(mainFrame, bg="#2C3E50")
    fSeason.pack(pady=10, fill="x")

    # Cria label de título para a tabela.
    cria_label(fSeason, "Quantidade de corridas por temporada", 12, "normal").pack(fill="x")

    # Cria a tabela de temporadas.
    seasonTabela = ttk.Treeview(fSeason, columns=("Temporada", "Corridas"), show="headings")
    seasonTabela.heading("Temporada", text="Temporada")
    seasonTabela.heading("Corridas", text="Qtd. Corridas")

    if temporadas:
        for tupla in temporadas:
            ano, qtd = tupla
            seasonTabela.insert("", "end", values=(ano, qtd))

    seasonTabela.pack(padx = 10, pady = 5, fill="x")

    overviewWindow.protocol("WM_DELETE_WINDOW", sair)
    overviewWindow.mainloop()


def abreOverview(connection, usuario):
    navigation.imprimeTracking()
    # Configura a janela principal.
    window = Toplevel()
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
        tipoCadastro = abreOverviewAdministrador(connection, window, usuario)
        cadastro.cadastrar(connection, tipoCadastro)
