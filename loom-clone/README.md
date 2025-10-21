# 🎥 Loom Clone - Enregistreur d'écran + Webcam

Un clone du logiciel Loom qui permet d'enregistrer simultanément votre écran et votre webcam, créant des vidéos de présentation professionnelles.

## ✨ Fonctionnalités

- **Enregistrement simultané** : Capturez votre écran et votre webcam en même temps
- **Interface graphique intuitive** : Interface simple et facile à utiliser
- **Prévisualisation en direct** : Voyez votre webcam avant d'enregistrer
- **Position personnalisable** : Placez votre webcam dans les 4 coins de l'écran
- **Qualité vidéo** : Enregistrement en 20 FPS pour des vidéos fluides
- **Format standard** : Vidéos sauvegardées en AVI

## 📋 Prérequis

- Python 3.7 ou supérieur
- Une webcam fonctionnelle
- Système d'exploitation : Windows, macOS ou Linux

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
cd loom-clone
```

### 2. Créer un environnement virtuel (recommandé)

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🎬 Utilisation

### Démarrer l'application

```bash
python loom_recorder.py
```

### Guide d'utilisation

1. **Lancez l'application** : Une fenêtre s'ouvre avec la prévisualisation de votre webcam

2. **Choisissez la position de la webcam** :
   - Top-left (en haut à gauche)
   - Top-right (en haut à droite)
   - Bottom-left (en bas à gauche)
   - Bottom-right (en bas à droite) - par défaut

3. **Démarrez l'enregistrement** :
   - Cliquez sur "⚫ Démarrer l'enregistrement"
   - L'enregistrement commence immédiatement
   - Le statut affiche "🔴 Enregistrement en cours..."

4. **Arrêtez l'enregistrement** :
   - Cliquez sur "⬛ Arrêter l'enregistrement"
   - La vidéo est automatiquement sauvegardée

5. **Trouvez vos vidéos** :
   - Les vidéos sont sauvegardées dans le dossier `recordings/`
   - Format du nom : `loom_recording_YYYYMMDD_HHMMSS.avi`

## 📁 Structure du projet

```
loom-clone/
│
├── loom_recorder.py      # Programme principal
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
└── recordings/           # Dossier des enregistrements (créé automatiquement)
```

## 🔧 Dépendances

- **opencv-python** : Capture de la webcam et traitement vidéo
- **numpy** : Manipulation des tableaux d'images
- **mss** : Capture d'écran haute performance
- **Pillow** : Traitement d'images pour l'interface

## 🎯 Fonctionnalités principales du code

### Classe `LoomClone`

La classe principale qui gère toute l'application :

- **`__init__()`** : Initialise l'interface et les paramètres
- **`setup_ui()`** : Crée tous les éléments de l'interface graphique
- **`start_preview()`** : Démarre la prévisualisation de la webcam
- **`start_recording()`** : Lance l'enregistrement dans un thread séparé
- **`record()`** : Fonction principale qui enregistre écran + webcam
- **`stop_recording()`** : Arrête l'enregistrement et sauvegarde la vidéo

### Processus d'enregistrement

1. Capture de l'écran avec `mss`
2. Capture de la webcam avec `cv2.VideoCapture`
3. Redimensionnement de la webcam (200x150 pixels)
4. Ajout d'un contour blanc autour de la webcam
5. Superposition de la webcam sur l'écran
6. Écriture de chaque frame dans le fichier vidéo

## 🛠️ Personnalisation

### Modifier la taille de la webcam

Dans `loom_recorder.py`, ligne 28 :

```python
self.webcam_size = (200, 150)  # Largeur, Hauteur
```

### Modifier le FPS (images par seconde)

Dans la fonction `record()`, ligne 194 :

```python
fps = 20.0  # Augmentez pour plus de fluidité, diminuez pour moins d'espace disque
```

### Modifier le format de sortie

Ligne 196-199 :

```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # AVI
# Alternatives :
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4
# fourcc = cv2.VideoWriter_fourcc(*'H264')  # H264
```

## 🐛 Dépannage

### La webcam ne s'affiche pas

- Vérifiez que votre webcam est connectée et fonctionnelle
- Essayez de fermer d'autres applications utilisant la webcam
- Sur Linux, assurez-vous d'avoir les permissions nécessaires

### L'enregistrement est lent ou saccadé

- Réduisez le FPS (par exemple à 15)
- Réduisez la taille de la webcam
- Fermez d'autres applications gourmandes en ressources

### Erreur lors de l'installation

Si vous avez des erreurs avec OpenCV sur Linux :

```bash
sudo apt-get install python3-opencv
# ou
pip install opencv-python-headless
```

## 💡 Conseils d'utilisation

1. **Testez d'abord** : Faites un court enregistrement de test pour vérifier que tout fonctionne
2. **Éclairage** : Assurez-vous d'avoir un bon éclairage pour la webcam
3. **Position** : Choisissez une position de webcam qui ne cache pas d'informations importantes
4. **Espace disque** : Les vidéos peuvent être volumineuses, vérifiez votre espace disque
5. **Conversion** : Vous pouvez convertir les AVI en MP4 avec VLC ou FFmpeg pour réduire la taille

## 🔄 Conversion vidéo (optionnel)

Pour convertir vos vidéos AVI en MP4 plus compacts :

```bash
# Avec FFmpeg
ffmpeg -i loom_recording_YYYYMMDD_HHMMSS.avi -c:v libx264 -crf 23 output.mp4
```

## 📝 Améliorations futures possibles

- [ ] Support du format MP4 directement
- [ ] Pause/Reprise de l'enregistrement
- [ ] Enregistrement audio (microphone)
- [ ] Annotation en temps réel
- [ ] Raccourcis clavier
- [ ] Upload automatique vers le cloud
- [ ] Compression vidéo automatique

## 📄 Licence

Ce projet est libre d'utilisation à des fins éducatives.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation

## 👨‍💻 Auteur

Créé avec Python et beaucoup de café ☕

---

**Bon enregistrement ! 🎬**
