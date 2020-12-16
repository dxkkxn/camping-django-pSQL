ALTER TABLE client
DROP CONSTRAINT client_num_emplacement_402f8e44_fk_emplacement_num_emplacement,
ADD CONSTRAINT num_emplacement_fk_client
FOREIGN KEY (num_emplacement) REFERENCES emplacement(num_emplacement)
ON DELETE CASCADE ;

ALTER TABLE responsable
DROP CONSTRAINT responsable_id_profil_49a78ebd_fk_profil_id_profil,
ADD CONSTRAINT id_profil_fk_responsable
FOREIGN KEY (id_profil) REFERENCES profil(id_profil) ON DELETE CASCADE ;

ALTER TABLE responsable
DROP CONSTRAINT responsable_num_client_3a79f6e1_fk_client_num_client,
ADD CONSTRAINT num_client_fk_responsable
FOREIGN KEY (num_client) REFERENCES client(num_client) ON DELETE CASCADE ;

ALTER TABLE responsable
DROP CONSTRAINT responsable_num_reservation_c14ad68f_fk_reservati,
ADD CONSTRAINT num_reservation_fk_responsable
FOREIGN KEY (num_reservation) REFERENCES reservation(num_reservation) ON DELETE CASCADE ;

ALTER TABLE responsable
DROP CONSTRAINT responsable_points_fidelite_8f9229c3_fk_fidelite_point_fidelite,
ADD CONSTRAINT points_fidelite_fk_responsable
FOREIGN KEY (points_fidelite) REFERENCES fidelite(point_fidelite) ON DELETE CASCADE ;



CREATE TABLE reservation_historique
(num_client INT, nom_client VARCHAR(30), prenom_client VARCHAR(30),
  debut_sejour DATE, fin_sejour DATE, type_emplacement VARCHAR(30))



CREATE OR REPLACE FUNCTION ajout_reservation_historique()
RETURNS trigger AS
$$
declare
num integer;
nom varchar(30);
prenom varchar(30);
dbsejour date;
fnsejour date;
tpemplacement varchar(30);
BEGIN
  SELECT num_client into num
  FROM responsable NATURAL JOIN client
  WHERE num_reservation = OLD.num_reservation;

  SELECT nom_client into nom
  FROM responsable NATURAL JOIN client
  WHERE num_reservation = OLD.num_reservation;

  SELECT prenom_client into prenom
  FROM responsable NATURAL JOIN client
  WHERE num_reservation = OLD.num_reservation;

  SELECT debut_sejour into dbsejour
  FROM reservation
  WHERE num_reservation = OLD.num_reservation;

  SELECT reservation.fin_sejour into fnsejour
  FROM reservation
  WHERE num_reservation = OLD.num_reservation;

  SELECT reservation.type_emplacement into tpemplacement
  FROM reservation
  WHERE num_reservation = OLD.num_reservation;

  INSERT INTO reservation_historique VALUES (num, nom, prenom, dbsejour,
    fnsejour, tpemplacement);
  RETURN OLD;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER ajout_reservation_historique
BEFORE DELETE
ON reservation FOR EACH ROW
EXECUTE PROCEDURE ajout_reservation_historique();
