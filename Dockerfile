# 1. Utiliser une image Python officielle légère
FROM python:3.10-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Installer les dépendances système minimales si nécessaire
# Installer d'abord torch en version CPU légère
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 4. Copier le fichier des dépendances (requirements.txt)
COPY requirements.txt .

# 5. Installer les bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier tout le reste du code (main.py ET ton dossier de modèle !)
COPY . .

# 7. Exposer le port sur lequel FastAPI va tourner (Hugging Face Spaces utilise souvent 7860)
EXPOSE 7860

# 8. Commande pour lancer l'API au démarrage du conteneur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]