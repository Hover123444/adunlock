# AdUnlock Discord + Site

Ce projet vous permet de générer des clés après visionnage de pubs pour débloquer un rôle Discord temporairement.

## Lancement

### 1. Lancer le site
```bash
cd web
pip install flask
python app.py
```

### 2. Lancer le bot
```bash
cd bot
pip install -r requirements.txt
python bot.py
```

### 3. Configuration
- Ajoutez votre token Discord dans `bot.py`
- Remplacez les "boutons pubs" dans `unlock.html` par vos vraies pubs
