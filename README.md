# SysF1_PostgreSQL

Sistema GUI em PostgreSQL para manipulação na base de dados de Fórmula 1. O projeto é proposto para a disciplina Laboratório de Base de Dados (SCC0641).

## 🤓 *Colaboradores:*
- [*Guilherme Castanon Silva Pereira*](https://github.com/GuilhermeCastanon);
- [*Hugo Hiroyuki Nakamura*](https://github.com/ikuyorih9);
- [*Isaac Santos Soares*](https://github.com/ISS2718);

## 📑 *Índice:*

## ⚙️ *Estrutura e funcionamento:*

### *Interface gráfica de usuário (GUI):*

### *Usuários*

Os usuários cadastrados no sistema devem ser salvos em uma tabela *Users*:

    CREATE TABLE Users (
        userid INTEGER,
        login VARCHAR(300),
        password VARCHAR(300),
        tipo VARCHAR(300),
        idoriginal INTEGER,
        CONSTRAINT PK_USERS PRIMARY KEY (userid),
        CONSTRAINT CK_USERS CHECK (tipo IN ('Administrador', 'Escuderia', 'Piloto'))
    );




