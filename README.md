# SysF1_PostgreSQL

<p align="center">
    <img src="https://img.shields.io/badge/Language-Python_3.12.7-gray?style=flat&labelColor=blue&link=https%3A%2F%2Fwww.postgresql.org%2F"/>
    <img src="https://img.shields.io/badge/Database-PostgreSQL-gray?style=flat&labelColor=yellow&link=https%3A%2F%2Fwww.postgresql.org%2F"/>
    <img src="https://img.shields.io/badge/GUI_Package-Tkinter-gray?style=flat&labelColor=purple&link=https%3A%2F%2Fdocs.python.org%2F3%2Flibrary%2Ftkinter.html"/>
    <img src="https://img.shields.io/badge/SQL_Package-Psycopg2-gray?style=flat&labelColor=purple&link=https%3A%2F%2Fimg.shields.io%2Fbadge%2FLanguage-Python_3.12.7-gray%3Fstyle%3Dflat%26labelColor%3Dblue%26link%3Dhttps%253A%252F%252Fwww.postgresql.org%252F
    "/>
</p>


Sistema GUI em PostgreSQL para manipulação na base de dados de Fórmula 1. O projeto é proposto para a disciplina Laboratório de Base de Dados (SCC0641).

## 🤓 *Colaboradores:*
- [*Guilherme Castanon Silva Pereira*](https://github.com/GuilhermeCastanon);
- [*Hugo Hiroyuki Nakamura*](https://github.com/ikuyorih9);
- [*Isaac Santos Soares*](https://github.com/ISS2718);

## 📑 *Índice:*

## ⚙️ *Estrutura e funcionamento:*

### *Usuários*

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

### *Telas e conexão:*

A interface gráfica é feita em *Python*, através do pacote **Tkinter**. Com ela, pode-ser criar telas, labels, botões etc. Os comandos SQL são realizados através do pacote **Psycopg2**.

A tela de ***Login*** apresenta um campo de *usuário* e de *senha*, e aguarda o botão de *sign in* para confirmar o acesso. A função executada pelo botão é a `login()`, que busca o login e senha da tabela ***Users*** e compara com o texto dos campos. Se o usuário estiver cadastrado, a próxima tela deve aparecer. Caso a correspondência seja falsa, uma *messagebox* é acionada para o login inválido.

```
def login():
        nonlocal returnValue
        usuario = Nome.get()
        senha = hashlib.md5(Senha.get().encode()).hexdigest()
        
        cursor = connection.cursor()
        cursor.execute("SELECT login, password FROM Users")
        users = cursor.fetchall()

        for user in users:
            login, password = user
            if login == usuario and password == senha:
                returnValue = 1
                window.quit()
                window.destroy()
                return
        
        messagebox.showerror("Login inválido", "Usuário ou senha incorretos.");
```
