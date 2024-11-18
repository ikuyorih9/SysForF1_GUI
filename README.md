![Formula 1 DBPG capa](./images/thumbnail/Formula1DBPG_thumbnail.jpeg)

<p align="center">
    <img src="https://img.shields.io/badge/Language-Python_3.12.7-gray?style=flat&labelColor=blue&link=https%3A%2F%2Fwww.postgresql.org%2F"/>
    <img src="https://img.shields.io/badge/Database-PostgreSQL-gray?style=flat&labelColor=yellow&link=https%3A%2F%2Fwww.postgresql.org%2F"/>
    <img src="https://img.shields.io/badge/GUI_Package-Tkinter-gray?style=flat&labelColor=purple&link=https%3A%2F%2Fdocs.python.org%2F3%2Flibrary%2Ftkinter.html"/>
    <img alt="Static Badge" src="https://img.shields.io/badge/SQL_Package-Psycopg2-gray?style=flat&labelColor=purple&link=https%3A%2F%2Fimg.shields.io%2Fbadge%2FLanguage-Python_3.12.7-gray%3Fstyle%3Dflat%26labelColor%3Dblue%26link%3Dhttps%253A%252F%252Fwww.postgresql.org%252F">
</p>

 Sistema GUI em PostgreSQL para manipulação na base de dados de Fórmula 1. O projeto é proposto para a disciplina Laboratório de Base de Dados (SCC0641).

# 🤓 *Colaboradores:*
- [*Guilherme Castanon Silva Pereira*](https://github.com/GuilhermeCastanon);
- [*Hugo Hiroyuki Nakamura*](https://github.com/ikuyorih9);
- [*Isaac Santos Soares*](https://github.com/ISS2718);

# 📑 *Índice*

1. [📅 **Tabelas do sistema**](#-colaboradores)
    - [Usuários](#usu%C3%A1rios)
    - [Logs de usuários](#logs-de-usu%C3%A1rio)
2. [🌐 **Conexão com a base de dados**](#-conex%C3%A3o)
3. [💻 **Telas**](#-telas)
    - [Login](#login)
    - [Overview]()
    - [Relatórios]()
4. [⚙️ **Configurações do sistema**]()
    - [Layout]()
    - [Navegação]()

# 📅 *TABELAS DO SISTEMA*

## *Usuários:*

Os usuários cadastrados no sistema devem ser salvos em uma tabela *Users*, contando com seu `userid` no sistema, seu `login`, `senha`, `tipo`, que pode ser 'Administrador', 'Escuderia' ou 'Piloto', `idoriginal`, que é o id na tabela original.

```
CREATE TABLE Users (
    userid INTEGER,
    login VARCHAR(300),
    password VARCHAR(300),
    tipo VARCHAR(300),
    idoriginal INTEGER,
    CONSTRAINT PK_USERS PRIMARY KEY (userid),
    CONSTRAINT CK_USERS CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto'))
);
```

A tabela é inicialmente preenchida com todos os pilotos e escuderias registrados, junto com um *admin*. Os `userid` são selecionados conforme ordem de carga na tabela. O ``login`` dos usuários são preenchidos conforme seu *nome de referencia*, concatenado com seu tipo ('_c' ou '_d'). A senha é seu próprio nome de referência, que é hashificada e salva na base. A função que realiza a carga na base é `CadastrarUsuarios()`.

```
CREATE OR REPLACE FUNCTION CadastrarUsuarios() RETURNS VOID AS $$
DECLARE
    i INTEGER := 1;
    login TEXT;
    password TEXT;
    id_original INTEGER;
    tipo TEXT;
BEGIN
    INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (0, 'admin', md5('admin'),'Administrador', NULL);

    FOR login, password, id_original, tipo IN
        (
            SELECT constructorref || '_c', md5(constructorref), constructorid, 'Escuderia'
            FROM Constructors
        )
        UNION
        (
            SELECT driverref || '_d', md5(driverref), driverid, 'Piloto'
            FROM Driver
        )
    LOOP

        INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (i, login, password,tipo, id_original);
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

Mudanças que são realizadas nas tabelas *Driver* e *Constructor* devem refletir na tabela de *Users*, isto é, o login e senha devem ser atualizados. Isso pode ser feito através de ***Triggers***, para *Delete*, *Insert* e *Update*. Para atualizar a tabela ***Driver***, o trigger `TR_atualizaPiloto` executa a função `atualizaPiloto()`.

```
CREATE OR REPLACE FUNCTION atualizaPiloto() RETURNS TRIGGER AS $$
DECLARE
    i INTEGER := 0;
    id_original INTEGER;
    driver_id INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT userid INTO i
        FROM Users
        ORDER BY userid DESC
        LIMIT 1;

        i := i + 1;

        INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (i, NEW.driverref || '_d', md5(NEW.driverref || '_d'), 'Piloto', NEW.driverid);

        RETURN NEW;

    ELSEIF TG_OP = 'UPDATE' THEN
        SELECT userid, NEW.driverid INTO i, driver_id
        FROM Users
        WHERE idoriginal = NEW.driverid AND
              tipo = 'Piloto';

        RAISE NOTICE 'Userid encontrado no update: (%,%)', i, driver_id;

        UPDATE Users
        SET 
            login = NEW.driverref || '_d',
            password = md5(NEW.driverref || '_d'),
            idoriginal = NEW.driverid
        WHERE userid = i; 

        RETURN NEW;

    ELSEIF TG_OP = 'DELETE' THEN
        DELETE FROM Users WHERE idoriginal = OLD.driverid AND tipo = 'Piloto';
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS TR_atualizaPiloto ON Driver;
CREATE OR REPLACE TRIGGER TR_atualizaPiloto AFTER DELETE OR INSERT OR UPDATE ON Driver
FOR EACH ROW EXECUTE FUNCTION atualizaPiloto();
```

Para a tabela *Constructors*, o trigger `TR_atualizaEscuderia` executa a função `atualizaEscuderia()`.

```
CREATE OR REPLACE FUNCTION atualizaEscuderia() RETURNS TRIGGER AS $$
DECLARE
    i INTEGER := 0;
    id_original INTEGER;
    constructor_id INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT userid INTO i
        FROM Users
        ORDER BY userid DESC
        LIMIT 1;

        i := i + 1;

        INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (i, NEW.constructorref || '_c', md5(NEW.constructorref || '_c'), 'Escuderia', NEW.constructorid);

        RETURN NEW;

    ELSEIF TG_OP = 'UPDATE' THEN
        SELECT userid, NEW.constructorid INTO i, constructor_id
        FROM Users
        WHERE idoriginal = NEW.constructorid AND
              tipo = 'Escuderia';

        RAISE NOTICE 'Userid encontrado no update: (%,%)', i, constructor_id;

        UPDATE Users
        SET 
            login = NEW.constructorref || '_c',
            password = md5(NEW.constructorref || '_c'),
            idoriginal = NEW.constructorid
        WHERE userid = i; 

        RETURN NEW;

    ELSEIF TG_OP = 'DELETE' THEN
        DELETE FROM Users WHERE idoriginal = OLD.constructorid AND tipo = 'Escuderia';
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS TR_atualizaEscuderia ON Constructors;
CREATE OR REPLACE TRIGGER TR_atualizaEscuderia AFTER DELETE OR INSERT OR UPDATE ON Constructors
FOR EACH ROW EXECUTE FUNCTION atualizaEscuderia();
```

## *Logs de usuário:*

Quando um usuário entra no sistema, sua conexão é registrada. Para isso, cria-se uma tabela ***Log_Table***, que armazena o seu `userid` e a `data` da conexão.

```
CREATE TABLE IF NOT EXISTS Log_Table(
    userid INTEGER,
    data TIMESTAMP,
    CONSTRAINT PK_LOG PRIMARY KEY (userid, data)
);
```

Quando um usuário faz o login no sistema, a função `registraLogin(userid)` é executada. Ela obtém a data/hora atual e realiza a inserção das informações necessárias na tabela. 

```
def registraLogin(userid):
    data = datetime.now()
    print(data)
    cursor.execute("INSERT INTO Log_Table(userid, data) VALUES (%s,%s);", (userid, data))
    connection.commit()
```

# 🌐 Conexão com a base de dados

Os comandos SQL são realizados através do pacote **Psycopg2**. Um arquivo `database.ini` contém as informações da base de dados a se conectar.

```
[postgresql]
dbname = Grupo2
user = Grupo2
password = grupo2-Hugo
host = 143.107.183.82
port = 5432
```

A conexão, portanto, é feita abrindo esse arquivo e utilizando a função `psycopg2.connect()`.

```
config = configparser.ConfigParser()
config.read('database.ini')

connection = psycopg2.connect(
    dbname = config['postgresql']['dbname'],
    user = config['postgresql']['user'],
    password = config['postgresql']['password'],
    host = config['postgresql']['host'],
    port = config['postgresql']['port']
)
```

Os comandos SQL são executados através de um cursor, que executa a função `execute()`.

```
cursor = connection.cursor()
cursor.execute("comando SQL")
connection.commit() # Para casos de insert, update ou delete.
```

# 💻 Telas do sistema

## *Login*

A interface gráfica é feita em *Python*, através do pacote **Tkinter**. Com ela, pode-se criar telas, labels, botões etc.

A tela de ***Login*** apresenta um campo de *usuário* e de *senha*, e aguarda o botão de *sign in* para confirmar o acesso. A função executada pelo botão é a `login()`, que busca o login e senha da tabela USERS e compara com o texto dos campos. Se o usuário estiver cadastrado, a próxima tela deve aparecer. Caso a correspondência seja falsa, uma *messagebox* é acionada para o login inválido. Se o *Sign up* acontecer, as informações de usuário são salvos numa tabela de LOGS.

```
def login():
    usuario = lNome.get()
    senha = hashlib.md5(lSenha.get().encode()).hexdigest()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE login = %s AND password = %s;", (usuario, senha))
    resultado = cursor.fetchone()
    if resultado:
        # Obtém o userid da busca.
        usuario = Usuario(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])

        # Salva o log de login
        data = datetime.now()
        cursor.execute("INSERT INTO Log_Table(userid, data) VALUES (%s,%s);", (usuario.userid, data))
        connection.commit()

        go_forward(window, lambda:abreOverview(connection, usuario))
        return
    else:
        print("NOT_FOUND_DB: usuario nao foi encontrado na base.")

    messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")
```

## Overview

A tela de ***Overview*** apresenta informações detalhadas sobre o usuário logado, que pode ser um **Piloto**, uma **Escuderia** ou um **Administrador**. Dependendo do tipo de usuário, diferentes informações e funcionalidades são exibidas.

#### Administrador

Apresenta informações para um usuário **Administrador**:

* **Quantidade de pilotos cadastrados;**

```
SELECT COUNT(DISTINCT driverid)
FROM Driver;
```
* **Quantidade de escuderias cadastradas**
```
SELECT COUNT(DISTINCT constructorid)
FROM Constructors;
```
* **Quantidade de pilotos por escuderia;**
```
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
```
* **Quantidade de circuitos cadastrados;**
```
SELECT COUNT(DISTINCT raceid)
FROM RACES;
```
* **Quantidade de corridas por circuito;**
```
SELECT Circuits.circuitid, Circuits.name, COUNT(DISTINCT raceid)
FROM RACES LEFT JOIN CIRCUITS ON Races.circuitid = Circuits.circuitid
GROUP BY (Circuits.circuitid, Circuits.name)
ORDER BY Circuits.circuitid
```
* **Quantidade de corridas por temporada.**
```
SELECT Seasons.year, COUNT(DISTINCT Races.raceid)
FROM Races LEFT JOIN Seasons ON Races.year = Seasons.year
GROUP BY Seasons.year
ORDER BY Seasons.year ASC;
```

### Escuderia

Apresenta informações para um usuário **Construtor**, como:

* **Quantidade e vitórias da escuderia;**
* **Quantidade de pilotos diferentes que já correram pela escuderia;**
* **Primeiro e último ano em que há dados da escuderia na base.**

### Piloto

Apresenta informações para um usuário **Piloto**, como:

* **Primeiro e último ano em que há dados do piloto na base;**
* **Para cada ano de competição e cada circuito, a quantidade de pontos obtidos;**
* **Para cada ano de competição e cada circuito, a quantidade de vitórias.**

### Relatórios

A tela de ***Relatório*** permite ao usuário visualizar relatórios detalhados baseados no tipo de usuário logado.

# ⚙️ Configurações do sistema

## Layout

Os layouts foram estabelecidos em códigos padrões, como uma interface entre o Tkinter e o usuário. Esses códigos são:

* **Criar uma Label:**
```
def cria_label(parent, text, fontsize=12, fontstyle="normal"):
    return Label(parent, text=text, compound="right", bg="#2C3E50", fg="#ECF0F1", font=("Montserrat", fontsize, fontstyle))
```

* **Criar um Button:**
```
def cria_botao(parent, text, fontsize=12, command = lambda:print("botão")):
    return  Button(parent, text=text, command=command, bg="#3498DB", fg="white", font=("Montserrat", fontsize), relief=GROOVE)
```

* **Criar uma Entry:**
```
def cria_entry(parent, backtext, fontsize=12, width=None, show=None):
    def on_entry_click(event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')

    def on_focusout(event, entry, placeholder):
        if entry.get() == ''):
            entry.insert(0, placeholder)
            entry.config(fg = 'grey')

    entry = Entry(parent, width=width, font=("Montserrat", fontsize), fg='grey', show=show)
    entry.bind('<FocusIn>', lambda event: on_entry_click(event, entry, backtext))
    entry.bind('<FocusOut>', lambda event: on_focusout(event, entry, backtext))
    entry.insert(0, backtext)
    return entry
```

* **Cria uma TreeView (tabela)**:
```
def cria_tabela(parent, columns, entries, stretch = True):
    # Cria a tabela de escuderias.
    table = ttk.Treeview(parent, columns=columns, show="headings")
    for column in columns:
        table.heading(column, text=column)
        table.column(column, anchor = "center", stretch=stretch)  # Largura fixa de 100px

    # Adiciona as escuderias na tabela
    if entries:
        for entry in entries:
            table.insert("", "end", values=entry)

    return table
```

* **Cria um Frame Scrollable**:
```
def cria_scrollable_frame(parent):
    # Evento para atualizar o tamanho do canvas quando os widgets são adicionados.
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width())
    
    # Evento para permitir rolagem com o mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Cria um canvas para a rolagem à esquerda.
    canvas = Canvas(parent, bg="#2C3E50")
    canvas.pack(side="left", fill="both", expand=True)

    # Cria uma barra de rolagem à direita.
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Coneta uma barra de rolagem ao canvas.
    canvas.configure(yscrollcommand=scrollbar.set)

    # Cria um frame geral para conter os widgets
    scrollableFrame = Frame(canvas, bg="#2C3E50")
    scrollable_frame_id = canvas.create_window((0,0), window=scrollableFrame, anchor="nw")
    scrollableFrame.bind("<Configure>", update_scroll_region)
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    return scrollableFrame
```

## Navegação

A navegação entre telas foi feita através de uma pilha `Navigation`, que empilha as telas conforme elas são chamadas e as desempilha conforme são fechadas.

Para voltar uma tela, executa-se a função `go_back(current_window)`, que recebe a janela atual a ser fechada.

```
def go_back(current_window):
    current_window.destroy()
    if Navigation:
        window = pop()
        if not window.winfo_viewable():
            window.deiconify()
```

Para avançar uma tela, executa-se a função `go_forward(current_window, function_next_window)`, que adiciona a `current_window` na pilha e executa a função `function_next_window` para abrir a nova tela.

```
def go_forward(current_window, function_next_window):
    push(current_window)
    if current_window.winfo_viewable():
        current_window.withdraw()
        current_window.quit()
    function_next_window()
```

Para fechar todas as telas, utiliza-se `close_all_windows(current_window)`, que fecha a janela principal `current_window` e todas as outras que estão na pilha de navegação.

```
def close_all_windows(current_window):
    current_window.destroy()
    while Navigation:
        window = pop()
        window.destroy()
```