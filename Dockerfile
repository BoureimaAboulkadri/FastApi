# Utiliser une image de base Python officielle
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copier les fichiers du projet dans le conteneur
COPY . .

# Commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
