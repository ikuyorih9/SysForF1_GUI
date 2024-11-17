from tkinter import *
from tkinter import ttk
from tkinter import Toplevel
from sources.cadastro import *
from sources.navigation import *
from sources.layouts import *
from sources.user import *

width = 1000
height = 600
def abreRelatorioPiloto(connection, window, usuario):
    cursor = connection.cursor()
    cursor.execute("""
   
    -- Consulta com ROLLUP
    SELECT 
        Races.year,
        Races.name AS corrida,
        COUNT(*) AS vitorias
    FROM Results
    JOIN Races ON Results.raceid = Races.raceid
    WHERE Results.driverid = %s AND Results.position = 1
    GROUP BY ROLLUP (Races.year, Races.name)
    ORDER BY Races.year, Races.name;

    """, (usuario.idoriginal,))

    resultado = cursor.fetchall()

    mainFrame = cria_scrollable_frame(window)
    fHeader = Frame(mainFrame, bg="#2C3E50")
    fHeader.pack(padx=10, pady=5, side="top", fill="x",expand=True)
    cria_botao(fHeader, "Voltar", 12, lambda:go_back(window)).pack(side="left")

    # cria label para título.
    cria_label(fHeader, "Relatórios do Piloto", fontsize=24, fontstyle="bold").pack(pady=5, fill="x", expand=True, side="top")

    # REPORT 1 FRAME
    fReport1 = Frame(mainFrame, bg="#2C3E50")
    fReport1.pack(padx=10, pady=5, fill="x")
    cria_label(fReport1, "Quantidade de vitorias obtidas").pack(fill="x", expand=True)

    # cria tabela para resultados x status.
    cria_tabela(fReport1, ("Ano","Corrida","Vitorias"), resultado).pack(padx = 10, pady = 5, fill="x")

    cursor.execute("""
   
    SELECT 
        Status.status AS descricao_status,
        COUNT(*) AS quantidade
    FROM Results
    JOIN Status ON Results.statusid = Status.statusid
    WHERE Results.driverid = %s
    GROUP BY Status.status
    ORDER BY quantidade DESC;

    """, (usuario.idoriginal,))

    resultado2 = cursor.fetchall()

    # REPORT 2 FRAME
    fReport2 = Frame(mainFrame, bg="#2C3E50")
    fReport2.pack(padx=10, pady=5, fill="x")

    # cria label para a tabela.
    cria_label(fReport2, "Quantidade de resultados por status").pack(fill="x", expand=True)

    # cria tabela para segundo report.
    tabela2 = cria_tabela(fReport2, ("Status","Quantidade"), resultado2).pack(padx = 10, pady = 5, fill="x")
    tabela2.pack(padx = 10, pady = 5, fill="x")

    window.mainloop()

def abreRelatorioEscuderia(connection, window, usuario):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT constructors.name
        FROM constructors
        WHERE constructorid = %s;
        """, (usuario.idoriginal,))
    nomeEscuderia = cursor.fetchone()[0]

    # Seleciona todos os pilotos da escuderia e conta suas vitórias.
    cursor.execute("""
        SELECT 
            DRIVER.forename || ' ' || DRIVER.surname AS piloto,
            COUNT(CASE WHEN RESULTS.rank = 1 THEN 1 ELSE NULL END) AS vitorias
        FROM 
            DRIVER
        LEFT JOIN 
            RESULTS ON DRIVER.driverid = RESULTS.driverid AND RESULTS.constructorid = %s
        WHERE 
            DRIVER.driverid IN (SELECT DISTINCT driverid FROM RESULTS WHERE constructorid = %s)
        GROUP BY 
            DRIVER.forename, DRIVER.surname
        ORDER BY 
            vitorias DESC;
        """, (usuario.idoriginal, usuario.idoriginal,))
    tabelaPilotosVitorias = cursor.fetchall()

    # Seleciona todos os Status e conta as ocorrencias de cada um.
    cursor.execute("""
        SELECT STATUS.status, COUNT(RESULTS.statusid) AS quantidade
        FROM RESULTS
        JOIN STATUS ON RESULTS.statusid = STATUS.statusid
        WHERE RESULTS.constructorid = %s
        GROUP BY STATUS.status
        ORDER BY quantidade DESC;
        """, (usuario.idoriginal,))
    tabelaStatusQuantidade = cursor.fetchall()

    mainFrame = Frame(window,  bg="#2C3E50")
    mainFrame.pack(fill="both", expand=True)

    # HEADER FRAME.
    fHeader = Frame(mainFrame, bg="#2C3E50")
    fHeader.pack(padx=10, pady=5, side="top", fill="x",expand=True)

    cria_botao(fHeader, "Voltar", 12, lambda:go_back(window)).pack(side="left")
    # cria label para título.
    cria_label(fHeader, f"Relatórios da {nomeEscuderia}", fontsize=24, fontstyle="bold").pack(pady=5, fill="x", expand=True, side="top")

    # REPORT 1 FRAME
    fReport1 = Frame(mainFrame, bg="#2C3E50")
    fReport1.pack(padx=10, pady=5, fill="x")

    # cria label para a tabela.
    cria_label(fReport1, "Pilotos da escuderia e suas vitórias").pack(fill="x", expand=True)
    
    # cria tabela para piilotos x vitórias.
    tabela1 = ttk.Treeview(fReport1, columns=("Pilotos","Vitórias"), show="headings")
    tabela1.heading("Pilotos", text="Pilotos")
    tabela1.heading("Vitórias", text="Vitórias")

    if tabelaPilotosVitorias:
       for tupla in tabelaPilotosVitorias:
            pilotos, vitorias = tupla
            tabela1.insert("", "end", values=(pilotos, vitorias))

    tabela1.pack(padx = 10, pady = 5, fill="x")

    # REPORT 2 FRAME
    fReport2 = Frame(mainFrame, bg="#2C3E50")
    fReport2.pack(padx=10, pady=5, fill="x")

    # cria label para a tabela.
    cria_label(fReport2, "Status e suas ocorrências").pack(fill="x", expand=True)

    # cria tabela para aeroportos.
    tabela2 = ttk.Treeview(fReport2, columns=("Status", "Ocorrências"), show="headings")
    tabela2.heading("Status", text="Status")
    tabela2.heading("Ocorrências", text="Ocorrências")

    if tabelaStatusQuantidade:
       for tupla in tabelaStatusQuantidade:
            status, ocorrencias = tupla
            tabela2.insert("", "end", values=(status, ocorrencias))

    tabela2.pack(padx = 10, pady = 5, fill="x")
    
    window.mainloop()


def abreRelatorioAdmin(connection, window, usuario):
    cursor = connection.cursor()
    def buscar(cidade, tabela):
        cursor.execute("""
            SELECT city, iatacode, AIRPORTS.name, Earth_Distance(LL_to_Earth(AIRPORTS.latdeg , AIRPORTS.longdeg), LL_to_Earth(GEOCITIES15K.lat, GEOCITIES15K.long)), type
            FROM AIRPORTS RIGHT JOIN GEOCITIES15K ON AIRPORTS.city = GEOCITIES15K.name
            WHERE (type = 'medium_airport' OR type = 'large_airport') AND
                GEOCITIES15K.country = 'BR' AND
                Earth_Distance(LL_to_Earth(AIRPORTS.latdeg , AIRPORTS.longdeg), LL_to_Earth(GEOCITIES15K.lat, GEOCITIES15K.long)) <= 100000 AND
                GEOCITIES15K.name = %s;
        """, (cidade,))
        resultado = cursor.fetchall()
        if resultado:
            for item in tabela.get_children():
                tabela.delete(item)
            
            for tupla in resultado:
                print(cidade)
                print(tupla)
                tabela.insert("", "end", values=tupla)


    # QUERIES:
    cursor.execute("""
        SELECT status, COUNT(resultid)
        FROM Results LEFT JOIN Status ON Results.statusid = Status.statusid
        GROUP BY status
        ORDER BY status;
    """)
    status = cursor.fetchall()

    mainFrame = cria_scrollable_frame(window)
    # mainFrame = Frame(scrollFrame, bg="#2C3E50")
    # mainFrame.pack(fill="both", expand=True)

    # HEADER FRAME.
    fHeader = Frame(mainFrame, bg="#2C3E50")
    fHeader.pack(padx=10, pady=5, side="top", fill="x",expand=True)

    cria_botao(fHeader, "Voltar", 12, lambda:go_back(window)).pack(side="left")
    # cria label para título.
    cria_label(fHeader, "Relatórios do Administrador", fontsize=24, fontstyle="bold").pack(pady=5, fill="x", expand=True, side="top")

    # REPORT 1 FRAME
    fReport1 = Frame(mainFrame, bg="#2C3E50")
    fReport1.pack(padx=10, pady=5, fill="x")

    # cria label para a tabela.
    cria_label(fReport1, "Quantidade de resultados por Status").pack(fill="x", expand=True)
    
    # cria tabela para resultados x status.
    cria_tabela(fReport1, ("Status","Resultados"), status).pack(padx = 10, pady = 5, fill="x")

    # REPORT 2 FRAME
    fReport2 = Frame(mainFrame, bg="#2C3E50")
    fReport2.pack(padx=10, pady=5, fill="x")

    # cria label para a tabela.
    cria_label(fReport2, "Aeroportos brasileiros de médio/grande porte a menos de 100km da cidade.").pack(fill="x", expand=True)

    # cria tabela para aeroportos.
    tabela2 = cria_tabela(fReport2, ("Cidade","Cod. IATA", "Nome", "Distância (km)", "Tipo"), [])
    tabela2.pack(padx = 10, pady = 5, fill="x")

    fFormTabela = Frame(fReport2, bg="#2C3E50")
    fFormTabela.pack(padx = 10, side="right")

    eCidade = cria_entry(fFormTabela, "Nome da cidade")
    eCidade.grid(row = 0, column = 0, padx=15, pady=5, sticky = "nsew")

    bBuscar = cria_botao(fFormTabela, "Buscar", command = lambda:buscar(eCidade.get(),tabela2))
    bBuscar.grid(row = 0, column = 1, padx=15, pady=5, sticky = "nsew")
    

    window.mainloop()



def abreRelatorio(connection, usuario):
    # Configura a janela principal.
    window = Toplevel()
    window.title("Relatório")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda:go_back(window))

    # Função para carregar as informações conforme o tipo do usuário
    if usuario.tipo == 'Piloto':
        abreRelatorioPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreRelatorioEscuderia(connection, window, usuario)
    elif usuario.tipo == 'Administrador':
        abreRelatorioAdmin(connection, window, usuario)

    return