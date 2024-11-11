from tkinter import *
from tkinter import ttk, messagebox
from sources import user

width = 400
height = 300

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
              Results.constructorid = Constructors.constructorid AND Results.raceid = Races.raceid ORDER BY Races.year DESC LIMIT 1;
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

    ttk.Label(window, text="Período:", style="TLabel").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=f"Primeiro Ano: {primeiroano} Último Ano: {ultimoano}", style="TLabel").grid(row=4, column=1, padx=5, pady=5, sticky="w")

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
    title_label = ttk.Label(window, text="Informações da Escuderia", style="Title.TLabel")
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Adiciona labels de informações
    ttk.Label(window, text="Usuário:", style="TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=usuario.login, style="TLabel").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Nome:", style="TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=nome, style="TLabel").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(window, text="Quantidade de pilotos:", style="TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    ttk.Label(window, text=str(qtdPilotos), style="TLabel").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Centraliza as colunas
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

def abreOverviewAdministrador(connection, window, usuario):
    pass

def abreOverview(connection, usuario):
    # Configura a janela principal.
    window = Tk()
    window.title("Overview")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="#2C3E50")

    if usuario.tipo == 'Piloto':
        abreOverviewPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreOverviewEscuderia(connection, window, usuario)
    elif usuario.tipo == 'Administrador':
        abreOverviewAdministrador(connection, window, usuario)

    window.mainloop()
