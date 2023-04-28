#!/usr/bin/python3
from flask import Flask, Response, render_template, g
from flask import request
import requests
from flask import redirect, url_for
from flask import jsonify, make_response
from .database import Database
import datetime
from calendar import monthrange, month_name
import csv
import io
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
import atexit
from pytz import utc
import yaml
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from calendar import monthrange, month_name
import json
from flask import jsonify
import os
import tweepy
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
from .schema import declaration_insertion_schema, profil_schema
from .declaration import Declaration
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session
import hashlib
import uuid


app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
schema = JsonSchema(app)
auth = HTTPBasicAuth()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def telecharger_donnees():
    # Fonctionnalité A1
    with app.app_context():
        un = "https://data.montreal.ca/dataset/"
        deux = "49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/"
        trois = "6173de60-c2da-4d63-bc75-0607cb8dcb74/download/"
        quatre = "declarations-exterminations-punaises-de-lit.csv"
        url = un + deux + trois + quatre
        r = requests.get(url)
        if r.status_code != 200:
            print("Erreur lors de la lecture du service")

        r.encoding = 'utf-8'
        csvio = io.StringIO(r.text)
        data = []
        data = creer_liste(csvio)
        # Fonctionnalité B1
        anciene_liste = get_db().get_toutes_les_donnees()
        get_db().insert_bd(data)
        nouvelle_liste = get_db().get_toutes_les_donnees()
        nouvelle_declaration = list(set(nouvelle_liste) - set(anciene_liste))
        nouvelle_declaration_triee = sorted(nouvelle_declaration,
                                            key=lambda tup: tup[1])
        with open('nouvelle_declaration.txt', 'w') as fichier:
            csv.writer(fichier, delimiter=' ').writerows(
                nouvelle_declaration_triee)
        envoyer_courriel_au("nouvelle_declaration.txt")
        # Fonctionnalité B2
        # email: mbd1355@yahoo.com
        # mot de pass: t12345gho
        envoyer_au_twitter("nouvelle_declaration.txt")
        return redirect('/accueil')


# Fonctionnalité B1
def envoyer_courriel_au(fichier):
    if os.stat(fichier).st_size != 0:
        with open('templates/email.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for ligne in data:
                courriel = ligne["email"]
                envoyer_le_courriel(courriel)


# Fonctionnalité B1
def envoyer_le_courriel(courriel):
    source_address = "michaeljeorge77@gmail.com"
    destination_address = courriel
    body = "Bonjour, Voir la fichier ci-jointe."
    subject = "fichier!"
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source_address
    msg['To'] = destination_address
    msg['ReplyTo'] = courriel
    msg.attach(MIMEText(body, 'plain'))
    with open('nouvelle_declaration.txt', 'r') as fp:
        fichier = MIMEText(fp.read())
        fichier.add_header('Content-Disposition',
                           'attachment', filename="nouvelle_declaration.txt")
        msg.attach(fichier)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(source_address, "inf5190$")
    text = msg.as_string().encode('utf-8')
    server.sendmail(source_address, destination_address, text)
    server.quit()


# Fonctionnalité B2
def envoyer_au_twitter(fichier):
    nbr_declarations = 0
    if os.stat(fichier).st_size != 0:
        with open(fichier) as file:
            for ligne in file:
                nbr_declarations = nbr_declarations + 1
            nbr_declarations = str(nbr_declarations)
            msg = ("""Le nombre de nouvelles
            déclarations""" + " " + nbr_declarations)
            envoyer_msg_a_twitter(msg)


# Fonctionnalité B2
def envoyer_msg_a_twitter(noQuartier):
    valeur1 = 'nSZGqze2xil0xCrwINRHEXakA'
    valeur2 = 'eDlwGAbibZWcYfxrsbqRLT5jymZROblvCFR0496T4jOqutZaqD'
    valeur3 = '1373451307042881542-zpuGgqsCE6wU3nFEOT5lB3LMvlkcTF'
    valeur4 = 'XuywO35v41gpeKLVJUFyXMpD00KgkjZluYCJzJyyarFU6'
    auth = tweepy.OAuthHandler(valeur1, valeur2)
    auth.set_access_token(valeur3, valeur4)
    api = tweepy.API(auth)
    tweet = noQuartier
    try:
        status = api.update_status(status=tweet)
    except IOError:
        print("Error")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Duplicate Tweet or Twitter Refusal: {}".format(e))


# Fonctionnalité A1
@app.route('/accueil')
def entrer_page_accueil():
    return render_template('accueil.html')


# Fonctionnalité A4
@app.route('/doc')
def documentation():
    return render_template('doc.html')


# Fonctionnalité A2
@app.route('/formulaire', methods=['POST'])
def rechercher():
    n_quartier = request.form['nom_quartier']
    n_arrondissement = request.form['nom_arrondi']
    if len(n_quartier) == 0 or len(n_arrondissement) == 0:
        return redirect('/formulaire/' + "invalid")
    return redirect('/formulaire/' + n_quartier + '/' + n_arrondissement)


# Fonctionnalité A2
@app.route('/formulaire/invalid')
def afficher_invalid():
    message_error = "Erreur-des champs vides ou des entrées invalides."
    return render_template('accueil.html', message_error=message_error)


# Fonctionnalité A2
@app.route('/formulaire/<n_quartier>/<n_arrondissement>')
def afficher_liste(n_quartier, n_arrondissement):
    liste = get_db().get_quartier_arrondissement(n_quartier, n_arrondissement)
    if len(liste) == 0:
        return redirect('/formulaire/' + "invalid")
    return render_template('information.html', liste=liste)


def creer_liste(csv_fichier):
    data = []
    for row in csv.DictReader(csv_fichier):
        no_declaration = row["NO_DECLARATION"]
        date_declaration = row["DATE_DECLARATION"]
        date_insp_vispre = row["DATE_INSP_VISPRE"]
        nbr_extermin = row["NBR_EXTERMIN"]
        date_debuttrait = row["DATE_DEBUTTRAIT"]
        date_fintrait = row["DATE_FINTRAIT"]
        no_qr = row["No_QR"]
        nom_qr = row["NOM_QR"]
        nom_arrond = row["NOM_ARROND"]
        coord_x = row["COORD_X"]
        coord_y = row["COORD_Y"]
        longitude = row["LONGITUDE"]
        latitude = row["LATITUDE"]
        row = (int(no_declaration), date_declaration,
               date_insp_vispre, nbr_extermin,
               date_debuttrait, date_fintrait,
               no_qr, nom_qr, nom_arrond, float(coord_x),
               float(coord_y), float(longitude), float(latitude),)
        data.append(row)
    data_triee = sorted(data, key=lambda tup: tup[1])
    data_sans_doublon = list(dict.fromkeys(data_triee))
    return data_sans_doublon


@app.route('/courriel')
def envoyer_courriel():
    return render_template('courriel.html')


@app.route('/declaration')
def declarer_dates():
    return render_template('declarations.html')


# Fonctionaliés A4 ,A5
def retouner_difference_dates(t1, t2):
    t1 = datetime.datetime.strptime(t1, "%Y-%m-%d")
    t2 = datetime.datetime.strptime(t2, "%Y-%m-%d")
    return ((t2 - t1).days)


# Fonctionaliés A4 ,A5
def validate(date_text):
    verification = False
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        verification = True
    return verification


# Fonctionaliés A4 ,A5, A6
def prendre_liste(liste_specifiee):
    data = []
    for row in liste_specifiee:
        data1 = {"no_declaration": row[0], "date_declation": row[1],
                 "date_insp_vispre": row[2], "nbr_extermin": row[3],
                 "date_debuttrait": row[4], "date_fintrait": row[5],
                 "no_qr": row[6], "nom_qr": row[7], "nom_arround": row[8],
                 "coord_x": row[9], "coord_y": row[10], "longitude": row[11],
                 "latitude": row[12]}
        data.append(data1)
    return data


# Fonctionnalité A4 ET A5
@app.route('/declarations', methods=['GET'])
def prendre_entre_dates():
    du = request.args.get('du')
    au = request.args.get('au')
    if len(du) == 0 or len(au) == 0:
        msg_error = "Tous les champs sont obligatoires."
        return render_template('accueil.html', msg_error=msg_error)
    # valider le format d'une date.
    verification_format = validate(du)
    verification_format1 = validate(au)
    if verification_format or verification_format1:
        msg_error = "la date n'est pas au bon format."
        return render_template('accueil.html', msg_error=msg_error)
    # valider les jours entre deux dates.
    nombre_de_jours = retouner_difference_dates(du, au)
    if nombre_de_jours < 0:
        msg_error = """la première date doit etre moins ou
                     égale à la deuxième date ."""
        return render_template('accueil.html', msg_error=msg_error)
    liste_specifiee = get_db().declarer_liste(du, au)
    data = []
    data = prendre_liste(liste_specifiee)
    return jsonify(data), 200


# Fonctionalité A6
@app.route('/api/declarationsquartiers', methods=['GET'])
def declarer_tous_quartiers():
    nom = request.args.get('quartiers')
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    declaration = get_db().declarer_liste_quartier(nom, date1, date2)
    liste_tous_les_quartiers = declaration
    data = []
    data = prendre_liste(liste_tous_les_quartiers)
    return jsonify(data), 200


# Fonctionalité D1
@app.route('/api/declaration', methods=["POST"])
@schema.validate(declaration_insertion_schema)
def creer_declaration_extermination():
    donnees = request.get_json()
    if not valider_declaration(donnees):
        msg = "Tous les champs sont obligatoires."
        return jsonify({'messageErreur': msg}), 400
    # verification_format = validate(donnees)
    if validate(donnees["date"]):
        msg = "la date n'est pas au bon format"
        return jsonify({'messageErreur': msg}), 400
    declaration = Declaration(None, donnees["quartier"],
                              donnees["arrondissement"], donnees["adresse"],
                              donnees["date"], donnees["nomPrenom"],
                              donnees["description"])
    declaration = get_db().sauvgarder_declaration(declaration)
    return jsonify(declaration.asDictionary()), 201


# Fonctionalité D1
@app.route('/api/declaration', methods=["GET"])
def get_declarations():
    data = []
    declarations = get_db().lire_toute_declaration()
    for lign in declarations:
        data1 = {"id": lign[0], "quartier": lign[1],
                 "arrondissement": lign[2], "adresse": lign[3],
                 "date": lign[4], "nomPrenom": lign[5],
                 "description": lign[6]}
        data.append(data1)
    declarations = data
    return jsonify(declarations), 200


# Fonctionalité D1
def valider_declaration(donnees):
    quartier = donnees["quartier"]
    arrondissement = donnees["arrondissement"]
    adresse = donnees["adresse"]
    date = donnees["date"]
    nomPrenom = donnees["nomPrenom"]
    description = donnees["description"]
    if (len(quartier) == 0 or len(arrondissement) == 0 or
        len(adresse) == 0 or len(date) == 0 or
            len(nomPrenom) == 0 or len(description) == 0):
        return False
    return True


# Fonctionalité A6
@app.route('/infoquartier')
def get_information_quartier():
    return render_template('infoquartier.html')


# Fonctionalité D1
@app.route('/extermination')
def declarer_extermination():
    return render_template('declaration.html')


# Fonctionalité D2
@app.route('/api/declaration/<id>', methods=["DELETE"])
def supprimer_declaration(id):
    declaration_existe = get_db().lire_une_declaration(id)
    if declaration_existe is False:
        return "L'identifiant spécifié n'existe pas.", 404
    else:
        get_db().supprimer_une_declaration(id)
        return "La donnée a été supprimée avec succès.", 200


# Fonctionalité D4
users = {"inf5190": generate_password_hash("coursweb")}


@auth.verify_password
def verify_password(username, password):
    if (username in users and check_password_hash
       (users.get(username), password)):
        return username


# Fonctionalité D3, D4
@app.route('/api/declaration', methods=["DELETE"])
@auth.login_required
def authentifier():
    format(auth.current_user())
    quartier = request.get_json()
    quartier = str(quartier)
    get_db().supprimer_toutes_quartiers(quartier)
    msg = "Les données ont été supprimée avec succès."
    return jsonify(msg), 200


# Fonctionalité E1
@app.route('/profile')
def entrer_profil():
    return render_template('profile.html')


# Fonctionalité E1
@app.route('/creerProfile')
def creer_profil():
    return render_template('creerProfile.html')


# Fonctionalité E1
@app.route('/api/profile', methods=["POST"])
@schema.validate(profil_schema)
def enregistrer_profile():
    donnees = request.get_json()
    nom = donnees["nom"]
    courriel = donnees["courriel"]
    liste = donnees["liste"]
    liste = liste.split()
    motPass = donnees["motPass"]
    if nom == "" or courriel == "" or liste == "" or motPass == "":
        return jsonify({'messageErreur':
                        "Tous les champs sont obligatoires."}), 400
    if (get_db().validate_profile(nom)):
        return jsonify({'messageErreur':
                        "le nom d'utilisateur a déjà été créé "}), 400
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(motPass + salt).
                                     encode("utf-8")).hexdigest()
    id = get_db().creer_profile(nom, courriel, salt, hashed_password)
    for item in liste:
        get_db().creer_quartier(id, item)
    msg = "Le profil a été créé avec succès."
    return jsonify(msg), 200


# Fonctionalité E2
@app.route('/modifierProfile')
def modifier_profil():
    return render_template('modifierProfile.html')


# Fonctionalité E2
@app.route('/validerprofile', methods=['POST', ])
def valider_profile():
    nom_utilisateur = request.form["nom"]
    mot_de_pass = request.form["motPass"]
    if nom_utilisateur == "" or mot_de_pass == "":
        message = "Tous les champs sont obligatoires."
        return render_template('modifierProfile.html', erreur=message)
    validation_de_nom = get_db().validate_profile(nom_utilisateur)
    if validation_de_nom is False:
        message = "l'utilisateur est inconnu."
        return render_template('modifierProfile.html', erreur=message)
    profile = get_db().prendre_profile(nom_utilisateur)
    id = profile[0]
    nom = profile[1]
    courriel = profile[2]
    salt = profile[3]
    hash = profile[4]
    hashed_password = hashlib.sha512(str(mot_de_pass + salt).
                                     encode("utf-8")).hexdigest()
    if hash != hashed_password:
        message = "le password n'est pas correct."
        return render_template('modifierProfile.html', erreur=message)
    id = str(id)
    return redirect('/' + id)


# FONCTIONNALITÉ E2
@app.route('/<int:id>')
def prendre_id_profile(id):
    id = int(id)
    profile = get_db().prendre_liste(id)
    return render_template('modifierlistequartier.html', profile=profile)


# FONCTIONNALITÉ E2(ajouter liste)
@app.route('/nouvelleliste', methods=['POST'])
def transfererId_pour_ajouter():
    id = request.form["id"]
    quartier = request.form["quartier"]
    if quartier == "":
        return redirect('/' + id + '/' + "quartier")
    return redirect('/' + id + '/' + quartier)


# FONCTIONNALITÉ E2(ajouter liste)
@app.route('/<id>/<quartier>')
def ajouter_dans_liste(id, quartier):
    liste = quartier.split()
    for item in liste:
        verification = get_db().verifier_quartiers(id, item)
        if verification is False:
            get_db().ajouter_quartiers(id, item)
    profile = get_db().prendre_liste(id)
    msg = "Les données ont été ajoutées avec succès."
    fichier = 'modifierlistequartier.html'
    return render_template(fichier, msg=msg,  profile=profile)


# FONCTIONNALITÉ E2(supprimer liste)
@app.route('/supprimerliste', methods=['POST'])
def transfererId_pour_supprimer():
    id = request.form["id"]
    quartier = request.form["quartier"]
    if quartier == "":
        return redirect('/' + id + '/' + "quartier")
    return redirect('/' + id + '/' + quartier + '/')


# FONCTIONNALITÉ E2(supprimer liste)
@app.route('/<id>/<quartier>/')
def supprimer_de_la_liste(id, quartier):
    liste = quartier.split()
    for item in liste:
        get_db().supprimer_quartiers(id, item)
    profile = get_db().prendre_liste(id)
    msg = "Les données ont été supprimées avec succès."
    fichier = 'modifierlistequartier.html'
    return render_template(fichier, msg=msg,  profile=profile)


# FONCTIONNALITÉ E2(ajouter et supprimer liste)
@app.route('/<id>/quartier')
def declarer_quartiers_erreur(id):
    profile = get_db().prendre_liste(id)
    message = "La liste vide n'est pas acceptée."
    fichier = 'modifierlistequartier.html'
    return render_template(fichier, erreur=message, profile=profile)


# FONCTIONNALITÉ E2(ajouter photo)
@app.route('/ajouterphoto', methods=['POST'])
def transfererId_photo():
    id = request.form["id"]
    photo = request.files["photo"]
    if photo:
        photo_id = str(uuid.uuid4().hex)
        get_db().ajouterPhotoId_au_profile(id, photo_id)
        get_db().creer_photos(photo_id, photo)
        return redirect('/' + id + '/' + "photoajouter")
    else:
        return redirect('/' + id + '/' + "photovide")


# FONCTIONNALITÉ E2(ajouter une photo avec succès)
@app.route('/<id>/photoajouter')
def ajouter_photo(id):
    profile = get_db().prendre_liste(id)
    msg = "La photo ajoute avec succès."
    fichier = 'modifierlistequartier.html'
    return render_template(fichier, msg=msg,  profile=profile)


# FONCTIONNALITÉ E2(ajouter une photo avec erreur)
@app.route('/<id>/photovide')
def declarer_photo_errur(id):
    profile = get_db().prendre_liste(id)
    message = "Vous n'avez pas choisi une photo."
    fichier = 'modifierlistequartier.html'
    return render_template(fichier, erreur=message, profile=profile)


# Fonctionnalité A3
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Canada/Eastern'})
func = telecharger_donnees
scheduler.add_job(func, 'cron', hour=00, minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
