PRAGMA foreign_keys = ON;

INSERT INTO Contatti (id, nome, cognome, telefono) VALUES
    (1, 'Mario', 'Rossi', '06-1234567'),
    (2, 'Luca', 'Bianchi', '02-9876543'),
    (3, 'Anna', 'Verdi', NULL),
    (4, 'Giulia', 'Neri', '06-7654321'),
    (5, 'Paolo', 'Serra', NULL);

INSERT INTO Gruppi (id_gruppo, nome_gruppo) VALUES
    (10, 'Lavoro'),
    (20, 'Famiglia'),
    (30, 'Universita'),
    (40, 'Sport');

INSERT INTO Appartenenza (id_contatto, id_gruppo) VALUES
    (1, 10),
    (1, 20),
    (2, 30),
    (4, 10);
