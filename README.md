# Projets Python - Portfolio de Développement

Ce dépôt contient plusieurs projets Python indépendants, chacun dans son propre dossier avec sa documentation complète.

## 📁 Projets Disponibles

### 1. 🎥 [Loom Clone](./loom-clone/)

**Clone du logiciel Loom - Enregistreur d'écran avec webcam**

Un logiciel permettant d'enregistrer simultanément votre écran et votre webcam, créant des vidéos de présentation professionnelles.

**Caractéristiques principales :**
- Enregistrement simultané de l'écran et de la webcam
- Interface graphique intuitive avec Tkinter
- Prévisualisation en direct de la webcam
- Position personnalisable de la webcam (4 coins)
- Sauvegarde automatique des vidéos

**Technologies :**
- OpenCV pour la capture vidéo
- mss pour la capture d'écran
- Tkinter pour l'interface graphique

**Documentation complète :** [loom-clone/README.md](./loom-clone/README.md)

**Démarrage rapide :**
```bash
cd loom-clone
./install.sh  # Linux/macOS
# ou
install.bat   # Windows
```

---

### 2. 📈 [ML Trading Strategy for S&P 500](./ml-trading-sp500/)

**Stratégie de trading algorithmique avec Machine Learning**

Un système de trading quantitatif utilisant des réseaux de neurones LSTM pour prédire la direction du S&P 500 et optimiser l'allocation de portefeuille.

**Caractéristiques principales :**
- Prédiction du marché avec LSTM bidirectionnel
- Optimisation de portefeuille (Markowitz, Risk Parity)
- Backtesting avec coûts de transaction réalistes
- Plus de 60 indicateurs techniques et features
- Visualisations interactives des performances

**Technologies :**
- TensorFlow/Keras pour le deep learning
- GARCH pour la modélisation de volatilité
- yfinance pour les données de marché
- Pandas/NumPy pour l'analyse de données

**Documentation complète :** [ml-trading-sp500/README.md](./ml-trading-sp500/README.md)

**Démarrage rapide :**
```bash
cd ml-trading-sp500
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python main.py
```

---

## 🚀 Navigation

Chaque projet est **complètement indépendant** et possède :
- ✅ Son propre README avec documentation détaillée
- ✅ Son propre fichier `requirements.txt`
- ✅ Ses propres scripts d'installation
- ✅ Sa propre structure de dossiers

**Pour utiliser un projet :**
1. Naviguez vers le dossier du projet
2. Consultez son README.md
3. Suivez les instructions d'installation spécifiques

## 📋 Structure du Dépôt

```
Project-Python-beginner-level-/
│
├── README.md                    # Ce fichier
├── .gitignore                   # Fichiers ignorés par Git
│
├── loom-clone/                  # Projet 1: Enregistreur d'écran
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── requirements.txt
│   ├── loom_recorder.py
│   ├── install.sh/bat
│   └── run.sh/bat
│
└── ml-trading-sp500/            # Projet 2: Trading ML
    ├── README.md
    ├── requirements.txt
    ├── main.py
    ├── config.py
    ├── setup.sh/bat
    ├── src/
    ├── notebooks/
    ├── data/
    ├── models/
    └── results/
```

## 🛠️ Prérequis Généraux

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Environnement virtuel (recommandé)

## 📝 Notes Importantes

⚠️ **Les projets sont indépendants :**
- Chaque projet a ses propres dépendances
- Utilisez des environnements virtuels séparés
- Les instructions d'installation sont dans chaque projet

⚠️ **Documentation :**
- Consultez le README de chaque projet pour plus de détails
- Chaque projet a sa propre documentation complète
- Ne confondez pas les instructions entre projets

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour chaque projet :
1. Consultez le README du projet spécifique
2. Suivez les guidelines de contribution du projet
3. Créez des pull requests séparées par projet

## 📄 Licence

Voir le fichier LICENSE dans chaque projet pour les détails spécifiques.

---

**Choisissez un projet ci-dessus et consultez sa documentation pour commencer !**
