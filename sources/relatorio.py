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
    # QUERIES:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT status, COUNT(resultid)
        FROM Results LEFT JOIN Status ON Results.statusid = Status.statusid
        GROUP BY status
        ORDER BY status;
    """)
    status = cursor.fetchall()



    mainFrame = cria_scrollable_frame(window)

    # HEADER FRAME.
    fHeader = Frame(mainFrame, bg="#2C3E50")
    fHeader.pack(padx=10, pady=5, side="top")

    # cria label para título.
    cria_label(fHeader, "Relatórios do Administrador", fontsize=24, fontstyle="bold").pack(pady=5, fill="x")

    # REPORT 1 FRAME
    fReport1 = Frame(mainFrame, bg="#2C3E50")
    fReport1.pack(padx=10, pady=5, fill="x", side="left")

    # cria label para a tabela.
    cria_label(fReport1, "Quantidade de resultados por Status").pack(fill="x", expand=True)
    
    # cria tabela para resultados x status.
    cria_tabela(fReport1, ("Status","Resultados"), status).pack(padx = 10, pady = 5, fill="x")

    # REPORT 2 FRAME
    fReport2 = Frame(mainFrame, bg="#2C3E50")
    fReport2.pack(padx=10, pady=5, fill="x", side="right")

    # cria label para a tabela.
    cria_label(fReport2, "Quantidade de resultados por Status").pack(fill="x", expand=True)
    
    # cria tabela para resultados x status.
    cria_tabela(fReport2, ("Status","Resultados"), status).pack(padx = 10, pady = 5, fill="x")

    # FOOTER FRAME.
    fFooter = Frame(mainFrame, bg="#2C3E50")
    fFooter.pack(padx=10, pady=5, fill="x", side="bottom")

    cria_botao(fFooter, "Logout", 12, lambda:go_back(window)).pack(side="left")

    window.mainloop()



def abreRelatorio(connection, usuario):
    # Configura a janela principal.
    window = Toplevel()
    window.title("Relatório")
    window.geometry(f"{width}x{height}")
    window.resizable(True, True)
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda:close_all_windows(window))

    # Função para carregar as informações conforme o tipo do usuário
    if usuario.tipo == 'Piloto':
        abreRelatorioPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreRelatorioEscuderia(connection, window, usuario)
    elif usuario.tipo == 'Administrador':
        abreRelatorioAdmin(connection, window, usuario)

    return