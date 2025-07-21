#!/usr/bin/env bash

# Arrête le script si une commande échoue
set -o errexit

# Collecte des fichiers statiques dans staticfiles/
python manage.py collectstatic --no-input

# Application des migrations (création de la base si elle n'existe pas encore)
python manage.py migrate
