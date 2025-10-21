#!/bin/bash

# Script de démarrage rapide pour Loom Clone

echo "🎥 Lancement de Loom Clone..."
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé!"
    echo "Veuillez d'abord exécuter: ./install.sh"
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier si les dépendances sont installées
if ! python -c "import cv2" &> /dev/null; then
    echo "❌ Dépendances manquantes!"
    echo "Veuillez d'abord exécuter: ./install.sh"
    exit 1
fi

# Lancer l'application
echo "✅ Démarrage de l'application..."
python loom_recorder.py
