from tkinter import *
from tkinter import messagebox
from sources import user
from tkinter import PhotoImage
from PIL import Image, ImageTk

width = 400
height = 300

def abreOverviewPiloto(connection, window, usuario):
    if usuario == None:
        return -1 

    returnValue = -1
    nome = "unknown"
    ano=-1
    tipo = ""
    idoriginal = ""
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
                Results.constructorid = Constructors.constructorid AND 
                Results.raceid = Races.raceid ORDER BY Races.year DESC LIMIT 1;
        """, (idoriginal,))
        resultado = cursor.fetchone()
        escuderia, ano = resultado

        # Busca o período de atuação do piloto (primeiro_ano, ultimo_ano)
        cursor.execute("""
            SELECT MIN(Races.year) AS primeiro_ano, MAX(Races.year) AS ultimo_ano
            FROM Results 
                JOIN Constructors ON Results.constructorid = Constructors.constructorid
                JOIN Races ON Results.raceid = Races.raceid
            WHERE Results.driverid = %s;
        """, (idoriginal,))
        primeiroano,ultimoano = cursor.fetchone()

        cursor.execute("""
        SELECT Races.year, Circuits.name AS circuito, 
            SUM(Results.points) AS total_pontos, 
            SUM(CASE WHEN Results.position = 1 THEN 1 ELSE 0 END) AS total_vitorias
        FROM Results
        JOIN Races ON Results.raceid = Races.raceid
        JOIN Circuits ON Races.circuitid = Circuits.circuitid
        WHERE Results.driverid = %s
        GROUP BY Races.year, Circuits.name
        ORDER BY Races.year, Circuits.name;
        """, (idoriginal,))

        resultado2 = cursor.fetchall()


    # Adiciona label de usuário na tela.
    Label(window, text="Usuário: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=usuario.login).grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de nome na tela.
    Label(window, text="Nome: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    Label(window, text=nome).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Adiciona label de escuderia na tela.
    Label(window, text="Escuderia: ").grid(row=2, column=0, padx=5, sticky="w")
    Label(window, text=escuderia + ' (' + str(ano) + ')').grid(row=2, column=1, padx=5, pady=5, sticky="w")

     # Adiciona label de periodo ano na tela
    Label(window, text="Atividade: ").grid(row=3, column=0, padx=5, sticky="w")
    Label(window, text=str(primeiroano) + " - " + str(ultimoano)).grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
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


def abreOverviewAdministrador(connection, window, usuario):
    imagem_original = Image.open("./images/key.png")
    imagem_redimensionada = imagem_original.resize((12, 12))
    imagem = ImageTk.PhotoImage(imagem_redimensionada)  
      
    Label(window, text="Usuário: ").grid(row=0, column=0, padx=5, sticky="w")
    frame = Frame(window)
    frame.grid(row=0, column=1, padx=5, sticky="w")
    label = Label(frame, text=usuario.login + " ", image=imagem, compound="right")
    label.pack(pady=20)
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
    elif usuario.tipo == 'Administrador':
        abreOverviewAdministrador(connection,window,usuario)