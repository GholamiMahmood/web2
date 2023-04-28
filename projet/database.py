import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/donnees.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Fonctionnalité A1
    def insert_bd(self, data):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(" DELETE FROM declaration")
        cursor.executemany("""INSERT INTO declaration
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", data)
        connection.commit()

    def get_toutes_les_donnees(self):
        cursor = self.get_connection().cursor()
        sql = """select * from declaration ORDER BY no_declaration """
        cursor.execute(sql)
        donnees = cursor.fetchall()
        return donnees

    # Fonctionnalité A2
    def get_quartier_arrondissement(self, nom_quartier, nom_arrondissement):
        cursor = self.get_connection().cursor()
        sql = """SELECT * FROM declaration WHERE nom_qr=? and nom_arround=?"""
        cursor.execute(sql, (nom_quartier, nom_arrondissement,))
        liste = cursor.fetchall()
        return liste

    # Fonctionaliés A4 ,A5
    def declarer_liste(self, du, au):
        cursor = self.get_connection().cursor()
        sql = """SELECT * FROM declaration WHERE date_debuttrait>=?
        and date_fintrait<=?"""
        cursor.execute(sql, (du, au,))
        liste = cursor.fetchall()
        return liste

    # Fonctionalité A6
    def declarer_liste_quartier(self, quartier, premierDate, deuxiemeDtae):
        cursor = self.get_connection().cursor()
        sql = """SELECT * FROM declaration WHERE
        nom_qr=? and date_debuttrait>=? and date_fintrait<=?
        ORDER BY nom_arround"""
        cursor.execute(sql, (quartier, premierDate, deuxiemeDtae, ))
        liste = cursor.fetchall()
        return liste

    # Fonctionalité D1
    def sauvgarder_declaration(self, declaration):
        connection = self.get_connection()
        if declaration.id is None:
            connection.execute("""insert into tab_extermination(quartier,
                                arrondissement, adresse, date, nom_prenom,
                                description ) values(?, ?, ?, ?, ?, ?)""",
                               (declaration.quartier,
                                declaration.arrondissement,
                                declaration.adresse,
                                declaration.date, declaration.nomPrenom,
                                declaration.description))
            connection.commit()

            cursor = connection.cursor()
            cursor.execute("select last_insert_rowid()")
            result = cursor.fetchall()
            declaration.id = result[0][0]
        else:
            connection.execute("""update declaration set quartier = ?,
                               arrondissement = ?,adresse = ?, date = ?,
                               nom_prenom = ?, description = ?
                               where rowid = ?""",
                               (declaration.quartier,
                                declaration.arrondissement,
                                declaration.adresse, declaration.date,
                                declaration.nomPrenom, declaration.description,
                                declaration.id))
            connection.commit()
        return declaration

    def lire_toute_declaration(self):
        cursor = self.get_connection().cursor()
        sql = """select * from tab_extermination ORDER BY id """
        cursor.execute(sql)
        donnees = cursor.fetchall()
        return donnees

    # Fonctionalité D2
    def lire_une_declaration(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tab_extermination where id=?", (id,))
        declaration = cursor.fetchall()
        if len(declaration) == 0:
            return False
        else:
            return True

    # Fonctionalité D2
    def supprimer_une_declaration(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tab_extermination where id=?", (id,))
        connection.commit()

    def supprimer_toutes_quartiers(self, quartier):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM declaration where nom_qr=?", (quartier,))
        connection.commit()

    def creer_profile(self, nom, courriel, salt, hash):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into profile(nom, courriel,"
                        "salt, hash) values(?, ?, ?, ?)"),
                       (nom, courriel, salt, hash))
        cursor.execute("select last_insert_rowid()")
        profile_id = cursor.fetchone()[0]
        connection.commit()
        return profile_id

    def creer_quartier(self, profile_id, nom_quartier):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into quartiers(profile_id, nom_quartier)"
                        "values(?, ?)"), (profile_id, nom_quartier, ))
        connection.commit()

    def validate_profile(self, nom):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile where nom=?", (nom,))
        declaration = cursor.fetchone()
        if declaration is None:
            return False
        else:
            return True

    def prendre_profile(self, nom):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM profile where nom=?", (nom,))
        declaration = cursor.fetchone()
        return declaration

    def prendre_liste(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM quartiers where profile_id=?", (id,))
        liste = cursor.fetchall()
        return liste

    def ajouter_quartiers(self, id, item):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into quartiers(profile_id, nom_quartier)"
                        "values(?, ?)"), (id, item, ))
        connection.commit()

    def verifier_quartiers(self, id, item):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM quartiers
        where profile_id=? and nom_quartier=?""", (id, item,))
        resultat = cursor.fetchone()
        if resultat is None:
            return False
        else:
            return True

    def supprimer_quartiers(self, id, item):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM quartiers
        where profile_id=? and nom_quartier=?""", (id, item,))
        connection.commit()

    def ajouterPhotoId_au_profile(self, id, photo_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        sql = """UPDATE profile SET photo_id=? WHERE id=?"""
        cursor.execute(sql, (photo_id, id,))
        connection.commit()

    def creer_photos(self, photo_id, file_data):
        connection = self.get_connection()
        cursor = connection.cursor()
        photo = [photo_id, sqlite3.Binary(file_data.read())]
        cursor.execute(("insert into photos(id, data)"
                        "values(?, ?)"), photo)
        connection.commit()
