[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com)

# LITReview

Application qui permet de demander/publier des critiques de livres/d'articles,
y associer une note, et la possibilité de suivre et être suivis par les autres utilisateurs.

## Démarrage

Une fois l'appliction télécharger, pour mettre en place :

1. A partir de votre terminal, se mettre au niveau du répertoire "LITReview".


2. Créer un environnement virtuel avec la commande:

   `python3 -m venv venv` ou `py -m venv venv`


3. Activer l'environnement virtuel:

   `venv\Scripts\activate`


4. Installer les bibliothèques nécessaires depuis le répertoire "LITReview":

   `pip install -r requirements.txt`


5. Lancer le serveur Django:
   - Pour initialiser une base de donnée :
   
   
      `python3 manage.py makemigrations`
      `python3 manage.py migrate` 

   - Avec la base disponible :
   
      
      `py manage.py runserver` ou `python3 manage.py runserver` 


6. Utilisateurs déjà créés dans la base du projet:
   * Nom: `Nelly` Password: `Maux2pass`
   * Nom: `` Password: ``
   * Nom: `` Password: ``
   * Nom: `` Password: ``


7. Administrateur créé:
   * Nom: `admin` Password: `admin`