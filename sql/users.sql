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

SELECT MIN(Races.year) AS primeiro_ano, MAX(Races.year) AS ultimo_ano
FROM Results 
    JOIN Constructors ON Results.constructorid = Constructors.constructorid 
    JOIN Races ON Results.raceid = Races.raceid
WHERE Results.driverid = %s;

SELECT Races.year, Circuits.name AS circuito, 
            SUM(Results.points) AS total_pontos, 
            SUM(CASE WHEN Results.position = 1 THEN 1 ELSE 0 END) AS total_vitorias
        FROM Results
        JOIN Races ON Results.raceid = Races.raceid
        JOIN Circuits ON Races.circuitid = Circuits.circuitid
        WHERE Results.driverid = 1
        GROUP BY Races.year, Circuits.name
        ORDER BY Races.year, Circuits.name;

-- Seleciona os pilotos de cada escuderia.
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

-- Obtem quantidade de escuderias.
SELECT COUNT(DISTINCT constructorid)
FROM Constructors;

-- Obtem quantidade de pilotos por escuderia.
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

-- Quantidade de corridas cadastradas
SELECT COUNT(DISTINCT raceid)
FROM RACES;

-- Quantidade de corridas por circuito
SELECT Circuits.circuitid, Circuits.name, COUNT(DISTINCT raceid)
FROM RACES LEFT JOIN CIRCUITS ON Races.circuitid = Circuits.circuitid
GROUP BY (Circuits.circuitid, Circuits.name)
ORDER BY Circuits.circuitid


SELECT Seasons.year, COUNT(DISTINCT Races.raceid)
FROM Races LEFT JOIN Seasons ON Races.year = Seasons.year
GROUP BY Seasons.year
ORDER BY Seasons.year ASC;

SELECT * FROM DRIVER ORDER BY driverid DESC LIMIT 10;
SELECT * FROM USERS ORDER BY userid DESC LIMIT 10;

SELECT status, COUNT(resultid)
FROM Results LEFT JOIN Status ON Results.statusid = Status.statusid
GROUP BY status
ORDER BY status;

DROP INDEX IF EXISTS idx_country;
DROP INDEX IF EXISTS idx_cidade;
DROP INDEX IF EXISTS idx_type;
DROP INDEX IF EXISTS idx_airport_city;


CREATE INDEX idx_cidade ON GEOCITIES15K USING HASH (name);
CREATE INDEX idx_type ON AIRPORTS (type);
CREATE INDEX idx_airport_city ON AIRPORTS (city);
CREATE INDEX idx_piloto ON Results (driverid);

EXPLAIN ANALYZE
SELECT city, iatacode, AIRPORTS.name, Earth_Distance(LL_to_Earth(AIRPORTS.latdeg , AIRPORTS.longdeg), LL_to_Earth(GEOCITIES15K.lat, GEOCITIES15K.long)), type
FROM AIRPORTS RIGHT JOIN GEOCITIES15K ON AIRPORTS.city = GEOCITIES15K.name
WHERE (type = 'medium_airport' OR type = 'large_airport') AND
      GEOCITIES15K.country = 'BR' AND
      Earth_Distance(LL_to_Earth(AIRPORTS.latdeg , AIRPORTS.longdeg), LL_to_Earth(GEOCITIES15K.lat, GEOCITIES15K.long)) <= 100000 AND
      GEOCITIES15K.name = 'Joinville';

SELECT * FROM GEOCITIES15K WHERE country = 'BR'

-- Consulta com ROLLUP
SELECT 
    Races.year,
    Races.name AS corrida,
    COUNT(*) AS vitorias
FROM Results
JOIN Races ON Results.raceid = Races.raceid
WHERE Results.driverid = 1 AND Results.position = 1
GROUP BY ROLLUP (Races.year, Races.name)
ORDER BY Races.year, Races.name;

SELECT MIN(Races.year) AS primeiro_ano, MAX(Races.year) AS ultimo_ano
FROM Results 
    JOIN Constructors ON Results.constructorid = Constructors.constructorid
    JOIN Races ON Results.raceid = Races.raceid
WHERE Results.driverid = 1;

CREATE OR REPLACE FUNCTION AtividadePiloto(id INTEGER) RETURNS TABLE (PrimeiroAno INTEGER, UltimoAno INTEGER)AS $$
DECLARE
    PrimeiroAno INTEGER;
    UltimoAno INTEGER;
BEGIN
    SELECT DISTINCT year INTO PrimeiroAno
    FROM RESULTS JOIN RACES ON RESULTS.raceid = RACES.raceid
    WHERE RESULTS.driverid = id
    ORDER BY year ASC
    LIMIT 1;

    SELECT DISTINCT year INTO UltimoAno
    FROM RESULTS JOIN RACES ON RESULTS.raceid = RACES.raceid
    WHERE RESULTS.driverid = id
    ORDER BY year DESC
    LIMIT 1;

    RETURN QUERY SELECT PrimeiroAno, UltimoAno;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM AtividadePiloto(1);
SELECT AtividadePiloto(1);


