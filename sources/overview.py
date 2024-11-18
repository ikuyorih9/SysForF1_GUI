from tkinter import *
from tkinter import ttk
from tkinter import Toplevel
from sources.cadastro import *
from sources.navigation import *
from sources.layouts import *
from sources.user import *
from sources.relatorio import *
from PIL import Image, ImageTk

width = 1000
height = 600

def abreOverviewPiloto(connection, overviewWindow, usuario):
    if usuario is None:
        return -1

    cursor = connection.cursor()

    cursor.execute("SELECT forename || ' ' || surname FROM Driver WHERE driverid = %s;", (usuario.idoriginal,))
    nome = cursor.fetchone()[0]

    cursor.execute("""
        SELECT DISTINCT Constructors.name, Races.year 
        FROM Results, Constructors, Races 
        WHERE Results.driverid = %s AND 
            Results.constructorid = Constructors.constructorid AND 
            Results.raceid = Races.raceid ORDER BY Races.year DESC LIMIT 1;
    """, (usuario.idoriginal,))
    resultado = cursor.fetchone()
    escuderia, ano = resultado

    # CHAMADA FUNCAO PL-PGSQL PARA PRIMEIRA CONSULTA DO OVERVIEW DE PILOTO
    cursor.execute("""
        SELECT * FROM AtividadePiloto(%s);
    """, (usuario.idoriginal,))
    primeiroano, ultimoano = cursor.fetchone()

    #CHAMADA FUNCAO PL-PGSQL PARA SEGUNDA CONSULTA DO OVERVIEW DE PILOTO
    cursor.execute("""
        SELECT * FROM InfoCompeticoes(%s)
    """, (usuario.idoriginal,))
        
    resultado2 = cursor.fetchall()

    # FRAME PARA O CABEÇALHO
    fHeader = Frame(overviewWindow, bg="#2C3E50")
    fHeader.pack(padx=10, pady=5)

    # Adiciona o label para o título.
    lTitulo = cria_label(fHeader, "Informações do Piloto",fontsize=16, fontstyle="bold")
    lTitulo.grid(row=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Adiciona labels de usuário.
    cria_label(fHeader, "Usuário:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, usuario.login).grid(row=1, column=1, padx=5, pady=5, sticky="e")

    # Adiciona labels de nome.
    cria_label(fHeader, "Nome:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, nome).grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # Adiciona labels de escuderia.
    cria_label(fHeader, "Escuderia:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, f"{escuderia} ({ano})").grid(row=3, column=1, padx=5, pady=5, sticky="e")

    # Adiciona labels de período de atividade
    cria_label(fHeader, "Atividade:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    cria_label(fHeader, str(primeiroano) + " - " + str(ultimoano)).grid(row=4, column=1, padx=5, pady=5, sticky="e")
    
    # FRAME PARA AS TABELAS
    pilotoFrame = Frame(overviewWindow, bg="#2C3E50")
    pilotoFrame.pack(padx=10, pady=5, fill="x")

    pilotoTabela = ttk.Treeview(pilotoFrame, columns=("Ano", "Circuito", "Total_Pontos", "Total_Vitorias"), show="headings")
    pilotoTabela.heading("Ano", text="Ano")
    pilotoTabela.heading("Circuito", text="Circuito")
    pilotoTabela.heading("Total_Pontos", text="Total de Pontos")
    pilotoTabela.heading("Total_Vitorias", text="Total de Vitorias")

    if resultado2:
       for tupla in resultado2:
            ano, circuito, total_pontos, total_vitorias = tupla
            pilotoTabela.insert("", "end", values=(ano, circuito, total_pontos, total_vitorias))

    pilotoTabela.pack(fill="x")

    fFooter = Frame(overviewWindow, bg="#2C3E50")
    fFooter.pack(padx=10,pady=10, fill="x", side="bottom")

    cria_botao(fFooter, "Logout", 12, lambda:go_back(overviewWindow)).pack(side="left")
    cria_botao(fFooter, "Relatório", 12, lambda: go_forward(overviewWindow, lambda: abreRelatorio(connection, usuario) )).pack(side="right")

    overviewWindow.mainloop()

def abreOverviewEscuderia(connection, overviewWindow, usuario):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT constructors.name
        FROM constructors
        WHERE constructorid = %s;
        """, (usuario.idoriginal,))
    nomeEscuderia = cursor.fetchone()[0]

    cursor.execute("SELECT name FROM Constructors WHERE constructorid = %s;", (usuario.idoriginal,))
    nome = cursor.fetchone()[0]
    
    # Query para contar a quantidade de corridas ganhas por uma escuderia
    cursor.execute("""
        SELECT get_wins_by_constructor(%s);
    """, (usuario.idoriginal,))
    qtdCorridasGanhas = cursor.fetchone()[0]

    # Query para obter a lista das corridas ganhas com seus respectivos pilotos
    cursor.execute("""
        SELECT * FROM get_race_winners(%s);
    """, (usuario.idoriginal,))
    tabelaCorridasGanhas = cursor.fetchall()

    cursor.execute("""
        SELECT get_driver_count_by_constructor(%s)
    """, (usuario.idoriginal,))
    qtdPilotos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT * FROM get_distinct_drivers_by_constructor(%s);
    """, (usuario.idoriginal,))
    tabelaPilotos = cursor.fetchall()


    cursor.execute("""
        SELECT * FROM get_constructor_year_range(%s);
    """, (usuario.idoriginal,))
    primeiroAno, ultimoAno = cursor.fetchone()

    # Configura estilos
    titleTextSize = 24
    titleTextStyle = "bold"
    labelTextSize = 12
    labelTextStyle = "normal"

    fWindow = cria_scrollable_frame(overviewWindow)

    # Título
    title_label = cria_label(fWindow, f"Informações da {nomeEscuderia}", titleTextSize, titleTextStyle)
    title_label.pack(padx=10, pady=10)

    fInfos = Frame(fWindow, bg="#2C3E50")
    fInfos.pack(padx=10,pady=5)

    # Adiciona labels de informações
    cria_label(fInfos, "Usuário:", labelTextSize, labelTextStyle).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    cria_label(fInfos, usuario.login, labelTextSize, labelTextStyle).grid(row=1, column=1, padx=5, pady=5, sticky="e")

    cria_label(fInfos, "Nome:", labelTextSize, labelTextStyle).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    cria_label(fInfos, nome, labelTextSize, labelTextStyle).grid(row=2, column=1, padx=5, pady=5, sticky="e")

    cria_label(fInfos, "Vitórias:", labelTextSize, labelTextStyle).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    cria_label(fInfos, str(qtdCorridasGanhas), labelTextSize, labelTextStyle).grid(row=3, column=1, padx=5, pady=5, sticky="e")

    cria_label(fInfos, "Pilotos da Escuderia:", labelTextSize, labelTextStyle).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    cria_label(fInfos, str(qtdPilotos), labelTextSize, labelTextStyle).grid(row=4, column=1, padx=5, pady=5, sticky="e")

    cria_label(fInfos, "Atividade:", labelTextSize, labelTextStyle).grid(row=5, column=0, padx=5, pady=5, sticky="w")
    cria_label(fInfos, str(primeiroAno) + " - " + str(ultimoAno), labelTextSize, labelTextStyle).grid(row=5, column=1, padx=5, pady=5, sticky="e")

    # TABELA DE CORRIDAS GANHAS
    corridasGanhasFrame = Frame(fWindow, bg="#2C3E50")
    corridasGanhasFrame.pack(fill="x", pady=10)

    # Cria label de título para a tabela.
    cria_label(corridasGanhasFrame, "Corridas Ganhas", 12, "normal").pack(fill="x")

    # Cria a tabela de corridas ganhas.
    corridasGanhasTabela = ttk.Treeview(corridasGanhasFrame, columns=("Corrida", "Piloto"), show="headings")
    corridasGanhasTabela.heading("Corrida", text="Corrida")
    corridasGanhasTabela.heading("Piloto", text="Piloto")

    if tabelaCorridasGanhas:
        for tupla in tabelaCorridasGanhas:
            corida, piloto = tupla
            corridasGanhasTabela.insert("", "end", values=(corida, piloto))
    
    corridasGanhasTabela.pack(padx = 10, pady = 5, fill="x")

    # TABELA DE PILOTOS
    pilotosFrame = Frame(fWindow, bg="#2C3E50")
    pilotosFrame.pack(fill="x", pady=10)

    # Cria label de título para a tabela.
    cria_label(pilotosFrame, "Pilotos que correram pela escuderia", 12, "normal").pack(fill="x")

    # Cria a tabela de pilotos.
    pilotosTabela = ttk.Treeview(pilotosFrame, columns=("Piloto"), show="headings")
    pilotosTabela.heading("Piloto", text="Piloto")

    if tabelaPilotos:
        for tupla in tabelaPilotos:
            piloto = tupla
            pilotosTabela.insert("", "end", values=(piloto))
    
    pilotosTabela.pack(padx = 10, pady = 5, fill="x")

    fFooter = Frame(fWindow, bg="#2C3E50")
    fFooter.pack(padx=10,pady=10, fill="x", side="bottom")

    cria_botao(fFooter, "Logout", 12, lambda:go_back(overviewWindow)).pack(side="left")
    cria_botao(fFooter, "Relatório", 12, lambda: go_forward(overviewWindow, lambda: abreRelatorio(connection, usuario) )).pack(side="right")
    # Centraliza as colunas
    overviewWindow.grid_columnconfigure(0, weight=1)
    overviewWindow.grid_columnconfigure(1, weight=1)

    
    overviewWindow.mainloop()

def abreOverviewAdministrador(connection, overviewWindow, usuario):
    def cadastrarEscuderia():
        push(overviewWindow)
        imprimeTracking()
        if overviewWindow.winfo_viewable():
            overviewWindow.withdraw()
            overviewWindow.quit()
        cadastrar(connection, 2)

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
        SELECT Circuits.name, COUNT(DISTINCT raceid)
        FROM RACES JOIN CIRCUITS ON Races.circuitid = Circuits.circuitid
        GROUP BY (Circuits.name)
        ORDER BY Circuits.name
    """)
    circuitos = cursor.fetchall()

    cursor.execute("""
        SELECT Seasons.year, COUNT(DISTINCT Races.raceid)
        FROM Races JOIN Seasons ON Races.year = Seasons.year
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
    cria_botao(fHeader, "Cadastrar Piloto", 12, lambda: go_forward(overviewWindow, lambda: cadastrar(connection, 1))).grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
    cria_botao(fHeader, "Cadastrar Escuderia", 12, lambda: go_forward(overviewWindow, lambda: cadastrar(connection, 2))).grid(row=1, column=1, padx=15, pady=5, sticky="nsew")

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
            nome, qtd = tupla
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

    fFooter = Frame(mainFrame, bg="#2C3E50")
    fFooter.pack(padx=10,pady=10, fill="x", side="bottom")

    cria_botao(fFooter, "Logout", 12, lambda:go_back(overviewWindow)).pack(side="left")
    cria_botao(fFooter, "Relatório", 12, lambda: go_forward(overviewWindow, lambda: abreRelatorio(connection, usuario) )).pack(side="right")

    overviewWindow.mainloop()


def abreOverview(connection, usuario):
    imprimeUsuario(usuario)
    # Configura a janela principal.
    window = Toplevel()
    window.title("Overview")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda:close_all_windows(window))


    # Função para carregar as informações conforme o tipo do usuário
    if usuario.tipo == 'Piloto':
        abreOverviewPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreOverviewEscuderia(connection, window, usuario)
    elif usuario.tipo == 'Administrador':
        abreOverviewAdministrador(connection, window, usuario)
        
