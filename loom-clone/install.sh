#!/bin/bash

echo "=========================================="
echo "  Installation de Loom Clone"
echo "=========================================="
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 n'est pas installé!"
    echo "Veuillez installer Python 3.7 ou supérieur."
    exit 1
fi

echo "✅ Python 3 trouvé: $(python3 --version)"
echo ""

# Créer un environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ Environnement virtuel créé"
else
    echo "❌ Erreur lors de la création de l'environnement virtuel"
    exit 1
fi

# Activer l'environnement virtuel
echo ""
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo ""
echo "⬆️  Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo ""
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Installation terminée avec succès!"
    echo "=========================================="
    echo ""
    echo "Pour démarrer l'application:"
    echo "1. Activez l'environnement virtuel: source venv/bin/activate"
    echo "2. Lancez l'application: python loom_recorder.py"
    echo ""
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi
