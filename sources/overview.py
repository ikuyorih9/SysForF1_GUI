from tkinter import *
from tkinter import messagebox
from sources import user

width = 400
height = 300

def abreOverviewPiloto(connection, window, usuario):
    if usuario == None:
        return -1 

    returnValue = -1
    nome = "unknown"
    cursor = connection.cursor()

    # Pega uma (e única) tupla da resposta.
    idoriginal = usuario.idoriginal

    if idoriginal:
        # Busca o nome completo do piloto a partir do seu id original.
        cursor.execute("SELECT forename || ' ' || surname FROM Driver WHERE driverid = %s;", (idoriginal,))
        nome = cursor.fetchone()[0]

        # Busca a última escuderia que o piloto esteve associado (último ano que competiu)
        cursor.execute("""
        SELECT DISTINCT Constructors.name, Races.year 
        FROM Results, Constructors, Races 
        WHERE Results.driverid = %s AND 
              Results.constructorid = Constructors.constructorid AND Results.raceid = Races.raceid ORDER BY Races.year DESC LIMIT 1;
        """, (idoriginal,))
        escuderia = cursor.fetchone()[0]

    # Adiciona label de usuário na tela.
    Label(window, text="Usuário: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=usuario.login).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de nome na tela.
    Label(window, text="Nome: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=nome).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de escuderia na tela.
    Label(window, text="Escuderia: ").grid(row=2, column=0, padx=5, sticky="w")
    Label(window, text=escuderia).grid(row=2, column=1, padx=5, pady=5, sticky="w")

    window.mainloop()

def abreOverviewEscuderia(connection, window, usuario):

    
    cursor = connection.cursor()
    # Busca o nome completo do piloto a partir do seu id original.
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

    # Adiciona label de usuário na tela.
    Label(window, text="Usuário: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=usuario.login).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de nome na tela.
    Label(window, text="Nome: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=nome).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de quantidade de pilotos na tela.
    Label(window, text="Quantidade de pilotos: ").grid(row=2, column=0, padx=5, sticky="w")
    Label(window, text=str(qtdPilotos)).grid(row=2, column=1, padx=5, pady=5, sticky="w")

    window.mainloop()

def abreOverview(connection, usuario):
    
    # Configura a janela principal.
    window = Tk()
    window.title("Overview")
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)


    if usuario.tipo == 'Piloto':
        abreOverviewPiloto(connection, window, usuario)
    elif usuario.tipo == 'Escuderia':
        abreOverviewEscuderia(connection, window, usuario)