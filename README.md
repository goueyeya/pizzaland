# Projet Pizza Land

<div style="text-align:center;">
<img src="https://img.freepik.com/photos-gratuite/pizza-fraichement-italienne-tranche-fromage-mozzarella-ia-generative_188544-12347.jpg">
</div>

## Description du Projet
Le projet Pizza Land est une application web avancée développée en utilisant le framework Django de Python. L'objectif principal de cette application est de gérer une plateforme de vente de pizzas en ligne, offrant aux utilisateurs la possibilité de parcourir le menu, passer des commandes, et bénéficier d'une gestion de compte utilisateur.

## Fonctionnalités Principales
- **Menu interactif:** Affiche une liste complète de pizzas avec leurs descriptions et prix.
- **Gestion des commandes:** Les utilisateurs peuvent ajouter des pizzas à leur panier, passer des commandes.
- **Gestion du compte utilisateur:** Création de compte, connexion, déconnexion, et gestion des informations personnelles.

## Prérequis
- Python (version 3.9.7 ou supérieure)
- Django (version 3.2.8 ou supérieure)
- Pillow (version 8.4.0 ou supérieure)

## Installation
1. Clonez le repository: `git clone https://git.iut-orsay.fr/goueyey/webpizza.git`
2. Naviguez vers le répertoire du projet: `cd webpizza`
3. Installez les dépendances: `pip install -r requirements.txt`
4. Appliquez les migrations: `python manage.py migrate`

## Configuration
1. Créez un fichier `.env` à la racine du projet et configurez les variables d'environnement nécessaires (clé secrète Django, informations de base de données, etc.).

## Utilisation
1. Lancez le serveur Django: `python manage.py runserver`
2. Accédez à l'application dans votre navigateur: `http://127.0.0.1:8000/`

# Auteur 

- [Gaëtan Oueyeya ](https://git.iut-orsay.fr/goueyey)
