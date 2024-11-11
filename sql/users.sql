-- TABELA DE USERS
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
    userid INTEGER,
    login VARCHAR(300),
    password VARCHAR(300),
    tipo VARCHAR(300),
    idoriginal INTEGER,
    CONSTRAINT PK_USERS PRIMARY KEY (userid),
    CONSTRAINT CK_USERS CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto'))
);

-- FUNÇÃO DE CADASTRAR USUÁRIOS.
DROP FUNCTION IF EXISTS CadastrarUsuarios();
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
        RAISE NOTICE 'Number: %, Login: %, Senha: %, Tipo: %, ID: %', i,login, password, tipo, id_original;

        INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (i, login, password,tipo, id_original);
        i := i + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT CadastrarUsuarios();

-- TRIGGER E FUNÇÃO DE ATUALIZAR OS PILOTOS DA TABELA USERS.

DROP FUNCTION IF EXISTS atualizaPiloto();
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

-- TRIGGER E FUNÇÃO DE ATUALIZAR OS CONSTRUTORES DA TABELA USERS.

DROP FUNCTION IF EXISTS atualizaEscuderia();
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

-- TABELA DE LOGS

CREATE TABLE IF NOT EXISTS Log_Table(
    userid INTEGER,
    data TIMESTAMP,
    CONSTRAINT PK_LOG PRIMARY KEY (userid, data)
);

SELECT * FROM Log_Table;

SELECT * FROM USERS;

SELECT forename, surname, name
FROM Driver, Constructos
WHERE driverid = 13 AND 

SELECT * FROM DRIVER;
SELECT * FROM PITSTOPS;
SELECT * FROM DRIVERSTANDINGS;
SELECT * FROM Results;
SELECT * FROM CONSTRUCTORS;

SELECT * FROM Results WHERE driverid = 1;

SELECT driverid, constructorid
FROM Races, Driver, Constructor, Results
WHERE 

SELECT R.raceid, year, name
FROM Results Re, Races R
WHERE driverid = 1 AND Re.raceid = R.raceid;

SELECT DISTINCT Constructors.name, Races.year
FROM Results, Constructors, Races
WHERE Results.driverid = 159 AND
      Results.constructorid = Constructors.constructorid AND
      Results.raceid = Races.raceid
ORDER BY Races.year DESC;

SELECT forename || ' ' || surname FROM Driver WHERE driverid = 13;

SELECT Races.year, Circuits.name AS circuito, 
            SUM(Results.points) AS total_pontos, 
            SUM(CASE WHEN Results.position = 1 THEN 1 ELSE 0 END) AS total_vitorias
        FROM Results
        JOIN Races ON Results.raceid = Races.raceid
        JOIN Circuits ON Races.circuitid = Circuits.circuitid
        WHERE Results.driverid = 1
        GROUP BY Races.year, Circuits.name
        ORDER BY Races.year, Circuits.name;

SELECT constructorid, COUNT(DISTINCT driverid)
FROM RESULTS, RACES
WHERE Races.raceid = Results.raceid AND
      (driverid, year) IN (
        SELECT DISTINCT driverid, MAX(year)
        FROM RESULTS, RACES
        WHERE Races.raceid = Results.raceid
        GROUP BY (driverid)
        ORDER BY driverid
      )
GROUP BY constructorid
ORDER BY constructorid;

-- Ultimo ano que um piloto correu.
SELECT DISTINCT driverid, MAX(year)
FROM RESULTS, RACES
WHERE Races.raceid = Results.raceid
GROUP BY (driverid)
ORDER BY driverid;

SELECT DISTINCT ON (driverid, constructorid)driverid, constructorid, year
FROM RESULTS, RACES
WHERE Races.raceid = Results.raceid
ORDER BY driverid, constructorid, year DESC;

SELECT * FROM USERS WHERE tipo = 'Escuderia';