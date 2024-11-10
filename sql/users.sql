CREATE TABLE Users (
    userid INTEGER,
    login VARCHAR(300),
    password VARCHAR(300),
    tipo VARCHAR(300),
    idoriginal INTEGER,
    CONSTRAINT CK_USERS CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto'))
);

INSERT INTO Users (userid, login, password, tipo, idoriginal) VALUES (0, 'admin', 'admin','Administrador', NULL);

SELECT * FROM Users;