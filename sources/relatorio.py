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
    window.mainloop()

def abreRelatorioEscuderia(connection, window, usuario):
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
    window.resizable(True, True)
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