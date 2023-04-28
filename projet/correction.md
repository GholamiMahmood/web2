# REMARQUES

1)Pour validation de html5, je l'ai validé et corrigé toutes les erreurs. Par contre, j'ai essayé plusieurs possibilités pour valider `url_for()` mais je n'arrive pas le faire.   

2)Pour chaque fonctionnalité, un commentaire avec son nom est écrit dans les fichiers de codes.   

Par exemple, tous les codes correspondants à la fonctionnalité A1 est écrit dessous d'un commentaire comme `# FONCTIONNALITÉ A1`.   

3)Avant d'exécution du programme, il faut effacer le fureteur. 

4)__Les fonctionnalités implémentées__

A1, A2, A3, A4, A5 et A6

B1, B2

D1, D2, D3 et D4

E1 et E2

----

## A1

Tout d'abord, on créé notre base de données. Pour ce faire, sur le terminal on se déplace dans le dossier **bd** et on lance la commande  

```sh 
sqlite3 donnees.db 
``` 
Ensuite dans l'environnement sqlite on lance la commande  

```sh 
sqlite> .read donnees.sql 
``` 
Ensuite on exécute le logiciel avec la commande

```sh 
make 
```  

Ensuite sur le fureteur Google Chrome quand on entre l'url `http://localhost:5000/` et on fait `ENTER`, l'application télécharge les données. S'il n'y a pas d'errer, les données seront enregistrées dans la base de données. 

Test A1:  

1)Pour tester cette fonctionnalité, on peut supprimer le fichier de base de données `donnees.bd`.  Et répéter les étapes précédentes pour relancer le programme. Alors, la base de données va être rempli.  

2)Si dans l'environnement sqlite on entre la commande   

```sh 
  sqlite> select * from declaration; 
```  

Cela affiche les données qui étaient téléchargées et étaient sauvegardées dans la table `declaration`.  

En cas d'erreur on pourra voir un message d'erreur `Erreur lors de la lecture du service` sur la console de terminal.  

3)J'ai créé une fonctionne `insert_bd()` dans le fichier `database.py` pour insère les données dans la base de données.  

4)J'ai créé une table `declaration` dans le fichier  `donnees.sql`. 

----

## A2 

Après l'exécution de programme, lorsqu'on se déplace vers la page d'accueil avec url `http://localhost:5000/accueil`, On peut trouver un formulaire qui a deux champs. Un champ pour entrer le `Nom de quartier` et l'autre pour entre le `Nom d'arrondissement`. 

D'abord on doit remplir le formulaire et ensuite on doit appuyer sur le bouton de `Rechercher`. Si ça trouve l'information pertinente dans la base de données,

Les résultats de la recherche s’affichent sur une nouvelle page. L'url de ce page est `http://localhost:5000/formulaire`. 

Test A2 :    

1)Il faut entrer le nom de quartier et d'arrondissement qui est existé dans la base de données, on va voir la liste détectée.  

2)Cliquer sur le bouton `Rechercher`. Si on envoie des champs vides ou invalides, le système va retourner un message d'erreur. 

3)Les fonctions implémentés: 
     `rechercher(), afficher_liste() et afficher_invalid()` qui se trouvent dans le fichier `main.py`. 

----

## A3 

En bas de fichier `main.py`, il y a un `BackgroundScheduler`. Cela extrait les données de la ville de Montréal à chaque jour, à minuit, et mettre à jour les données de la base de données et recharge `http://localhost:5000/`. 

Test A3: dans le code, on peut changer hour et minute et on peut les mettre à un heur désiré. 

On peut lancer le programme et supprimer le fichier donnees.db.  

Lorsque l'horloge montre l'heure programmée. Un fichier donnees.db sera créé. Et les données seront extraits.

Si on lance la commande `select * from declaration;` on pourra voir les nouvelles données. La page `http://localhost:5000/` sera rechargé. 

----

## A4 

Test A4 :  

Sur le fureteur lancer l'url avec deux dates entrées. Par exemple `http://localhost:5000/declarations?du=2021-01-04&au=2021-04-22` 

Vous pourrez voir le résultat. 

Test RAML : Une route `http://localhost:5000/doc` est disponible et affiche la représentation HTML de la document RAML du service web. Dans le fichier `main.py` on la fonction `documentation()` qui fournit cette fonctionnalité. 

----

## A5 

On lance le logiciel et sur la page d'accueil avec l'url `http://localhost:5000/accueil`, on pourra voir une formulaire à droit de notre écran qui contient deux champs de dates `La première date` et `La deuxième date`. 

Lorsque on entre les deux dates et on lance la recherche, une requête Ajax contenant les deux dates saisies est envoyée à la route définie en A4. 

Lorsque la réponse Ajax revient, l'application affiche la liste des contrevenants dans un tableau dans la page d'accueil. 

Le tableau contient 3 colonnes `Arrondissement, Quartier et Nombre de declarations`. On trouve ce tableau à droit d'écran en bas. 

Test A5: 

1)Allez sur la page `http://localhost:5000/accueil`.

2)Remplissez deux champs de dates dans le formulaire, et puis appuyez sur le buton `Rechercher`. 

3)l'application affiche la liste des contrevenants dans un tableau dans la page d'accueil. 

4)Pour envoyer une requête Ajax, j'ai écrit une fonction `chercher()` qui se trouve dans le fichier `static/js/script.js`. 

5)Les fonctions implémentées:  

Dans le fichier main.py par les fonctions `prendre_entre_dates(), validate(), retourner_difference_dates(), prendre_liste()`et dans le fichier database.py les fonctions `declarer_liste()`. 

----

## A6 

Après tester la fonctionnalité A5 on pourra voir que la liste de tous les quartiers est prédéterminée dans une liste déroulante dans la page d'accueil `http://localhost:5000/accueil`. 

Cette liste déroulante se trouve à droite en bas du buton de `Rechercher` avec un label `Liste de quartier`. On peut choisir un quartier parmi cette liste.  

Test A6: 1)exécuter les mêmes étapes que dans le A5.  

      2)Si vous cliquez sur cette liste déroulant vous pourrez voir la liste de tous les quartiers.  

         Le contenu de la liste provient des noms de quartier dans la base de données. Dans le fichier main.py dans la section Fonctionnalité A6 il y a une fonction qui s'appelle `declarer_tous_quartiers()` dans cette fonction, j'ai appelé la fonction `get_db().declarer_liste_quartier()`  qui récupère la liste de quartiers et l'envoie vers le client.  

      3)Vous pouvez choisir un quartier parmi cette liste et ensuite appuyer sur le bouton `envoyer`.  

      4)La requête Ajax est envoyée au service REST du point A4 avec la fonction `changerQuartier()` qui se trouve dans le fichier **script.js**.  

      5)Le résultat sera affiché dans une page pop-up avec url `http://localhost:5000/infoquartier`.  

      6)Pour effectuer A6 dans le fichier **main.py** les fonctionnes `declarer_tous_quartiers(), prendre_liste()` et dans le fichier **database.py** la fonctionne `declarer_liste_quartier()` ont été implementée. 

----

## B1 

Dans le dossier template, il y a un fichier configuration **email.yaml** qui contient l'adresse du destinataire du courriel.  

Test B1:  

1)**Adresse destinataire**: pour tester vous pouvez utiliser l'adresse courriel `michaeljeorge77@gmail.com` et mot de passe `inf5190$`. Si vous voulez tester avec un adresse courriel de votre choix, vous pouvez remplacer l'adresse qui se trouve dans le fichier main.py dans la fonction `envoyer_le_courriel()` par l'adresse courriel de votre choix.  

2)**Adresse expéditeur**: Les adresses d'expéditeurs sont dans le fichier **template/email.yaml**. Vous pouvez utiliser la même adresse de numéro (1). Par contre vous pouvez ajouter une adresse de votre choix dans le fichier **template/email.yaml** et l'utiliser pour le test.  

3)Il faut effacer le fichier **db/donnees.db** pour vider les données de la base de données.  

4)Relancez le programme. Le fichier *nouvelle_declaration.txt* automatiquement sera créé. Et les nouvelles déclarations seront écrit dans ce fichier. le fichier *nouvelle_declaration.txt* sera envoyé aux adresses courriels qui sont dans le fichier **email.yaml**.  

5)Voilà, vous pouvez ouvrir le courriel et vous allez recevoir un fichier contenant le résultat. 

----

## B2   

Remarque:  

Pour effectuer cette fonctionnalité, J'ai créé un compte: `mbd1355@yahoo.com` avec le mot de pas: `t12345gho` pour le tester.  

et aussi j'ai créé un API dans la twitter avec l’information suivant :    

auth = tweepy.OAuthHandler('nSZGqze2xil0xCrwINRHEXakA','eDlwGAbibZWcYfxrsbqRLT5jymZROblvCFR0496T4jOqutZaqD')   

auth.set_access_token('1373451307042881542-zpuGgqsCE6wU3nFEOT5lB3LMvlkcTF','XuywO35v41gpeKLVJUFyXMpD00KgkjZluYCJzJyyarFU6')   

Test B2:  

1)D'abord, on doit effacer le fichier **db/donnees.db** pour vider les données de la base de données.  

2)Relancez le programme. Le fichier *nouvelle_declaration.txt* automatiquement sera créé. Et les nouvelles déclarations seront écrit dans ce fichier.  

3)La programme compte le nombre de linges de fichier nouvelle_declaration.txt, Si ce fichier n'est pas vide et s'il y des données dedans, la nombre de données sera envoyé à l’adresse de twitter.   

4)Dans cette étape, on doit s'authentifier au twitter avec le compte: `mbd1355@yahoo.com` et mot de pas: `t12345gho`.  

5)dans la section Profile vous pourrez voir le résultat.  

Pour B2, les fonctions implémentées dans le fichier main.py sont: `envoyer_au_twitter(fichier)` et  

`envoyer_msg_a_twitter(noQuartier)`. 

----

## D1   

Il y a dex façons pour tester cette fonctionnalité avec **YARC** ou en suivant les étapes suivantes.  

Test D1:   

1)Lancer le programme.  

2)Déplacer dans le page d'accueil avec l'url `http://localhost:5000/accueil`.  

3)À gauche de cette page, il y a un lien qui s'appelle `Envoyer nouvelle déclaration`. En cliquant sur ce lien, le système va vous diriger vers une page `declaration.html` avec l'url `http://localhost:5000/extermination`.  

4)Il y a un formulaire. On doit remplir les champs.  

5)Le système va valider les données avec un `jason-schema` qui se trouve dans le fichier `schema.py`. Et puis cela enregistre les données dans la BD et un message de réussi s'affiche en bas de bouton d'`Envoyer`.  

6)S'il y a des erreurs le système envoie un message d'erreur.  

7)Pour tester données de BD, sur la terminale, on doit entrer la commande   

```sh 
sqlite3 donnees.db 
``` 

Et puis, dans l'environnement SQLite on lance la commande 

```sh 
sqlite> select * from tab_extermination; 
``` 

vous pouvez voir le résultat.  

8)Le service est documenté avec RAML sur /doc.  

Test D1 avec **YARC**:  

On peut aller sur la page de `doc` avec url `http://localhost:5000/doc`. 

Dans la section /api/declaration on clique sur le POST. 

On peut prendre l'objet de documentation RAML et avec **YARC** envoyer une requête **POST** on pourra recevoir une réponse succès avec un body qui contient un objet declaration avec un id. 

----

## D2 

Test D2: 

On peut tester cette fonctionnalité avec **YARC**. 

On envoie une requête **DELETE** avec url `http://localhost:5000/api/declaration/<id>`. En cas de succès le système retourne le code 200 et un message de succès. 

Si id n'existe pas dans le BD le système retourne un code 404 avec un message d'erreur.  

Le service est documenté avec RAML sur /doc.  

Les fonctionnes implémentées dans `main.py` sont `supprimer_declaration(id)`, et dans le database.py sont `lire_une_declaration(id), supprimer_une_declaration(id)`.

----

## D3 et D4  

Premièrement, le fureteur doit être vidée.  

1)Lancer le programme.  

2)Allez sur la page `http://localhost:5000/accueil`.  

3)Remplissez deux champs de dates dans le formulaire, et puis appuyez sur le buton `Rechercher`.  

4)l'application affiche la liste des contrevenants dans un tableau dans la page d'accueil.  

(Si vous cliquez sur envoyer vous pouvez voir les déclarations pour ce quartier après suppression vous pourrez voir que les données seront enlevées.)  

5)Choisissez un quartier et puis appuyez sur le bouton **supprimer**.  

6)Une page pop-up est apparue. Vous pouvez entrer les informations suivantes pour s'authentifier.   

Nom d'utilisateur : `inf5190`   

Mot de passe : `coursweb`  

7)Ensuite cliquez sur le bouton `connexion`. Les données seront supprimées et un message de succès va être affiché.   

8)Pour être sûre de suppression de données, si vous cliquez sur le bouton envoyer, vous allez voir que la liste est vide.  

De plus, on peut tester le service de DELETE en utilisant le **YARC**. 

On envoie une requête **DELETE** avec url `http://localhost:5000/api/declaration`. En cas de succès le système retourne le code 200 et un message de succès.  

Le service est documenté avec RAML sur /doc. 

----

## E1  

Premièrement, le fureteur doit être vidée.  

1)Lancez le programme.  

2)Allez sur la page `http://localhost:5000/accueil`.  

3)En haut sur l'entête de la page il y a un icon de profile. Vous pouvez cliquer sur cet icone.  

4)Le système ouvre la page `profile.html` avec url `http://localhost:5000/profile`.  

5)Vous pouvez cliquer sur le bouton **Créer**.  

6)Le système ouvre la page **creerProfile.html** avec url `http://localhost:5000/creerProfile`. Il y a un formulaire dans cette page. On doit remplir les champs et appuyer sur le bouton **Envoyer**. En cas de succès, une profile sera créé et un message de succès sera affiché (pour quelques secondes).  

7)Le document JSON est validé avec **json-schema** qui se trouve dans le fichier **schema.py**. Le service est documenté avec RAML sur /doc. 

----

## E2  

1)Répéter les étapes de (1) à (4) du E1.  

2)Vous pouvez cliquer sur le bouton **Modifier**.  

3)En cas de succès, le système ouvre la page `modifierProfile.html` avec url `http://localhost:5000/modifierProfile`.  

5)Entrez le nom d'utilisateur et le mot de passe. Ensuite cliquez sur **Envoyer**.  

6)Le système vous dirige vers la page modifierListeQuartier.html avec url `http://localhost:5000/<id>`. Chaque utilisateur a un **id** unique dans le tableau de profile.  

7)Dans cette page on a 3 boutons **Ajouter** pour ajouter une liste de quartier, **Supprimer** pour l'effacer et il y a la possibilité de téléverser une photo avec le bouton **Choisir un fichier** et **Envoyer**.  

Lorsqu'on ajoute ou supprime des quartiers, on peut voir le résultat dans une table à gauche de cette page.  

De plus, pour téléverser une image, vous pouvez cliquer sur le bouton **Choisir un fichier** et choisir une image qui se trouve dans le dossier `static/img`. et appuyer sur **Envoyer**. 

En cas de succès on aura un message de succès. 

 