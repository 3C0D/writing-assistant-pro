# 🌐 Système de Traduction - Writing Assistant Pro

## 📖 Vue d'ensemble

Le système de traduction utilise **Babel** (gettext wrapper standard) avec **un seul script unifié** :

```bash
# UNE seule commande pour tout faire :
uv run python scripts/translation_management/update_translations.py
```

Ce script automatiquement :
1. 🔍 **Extrait** les textes à traduire du code (pybabel extract)
2. 🔄 **Synchronise** les fichiers .po pour toutes les langues (pybabel init/update)
3. ⚙️ **Compile** en format binaire (.mo) (pybabel compile)

---

## 🚀 Workflow pratique

### 1️⃣ **Au démarrage du projet**

```bash
# Lancer une fois pour créer le template
uv run python scripts/translation_management/extract_translations.py

# Créer les traductions initiales
uv run python scripts/translation_management/sync_translations.py

# Compiler pour l'application
uv run python scripts/translation_management/compile_translations.py
```

### 2️⃣ **Quand tu ajoutes du nouveau texte à traduire**

Tu fais ça dans le code :
```python
ui.label(_("Nouveau texte à traduire"))
```

Puis tu lances :
```bash
# 1. Extraire le nouveau texte
uv run python scripts/translation_management/extract_translations.py

# 2. Synchroniser les fichiers .po
uv run python scripts/translation_management/sync_translations.py

# 3. Compiler
uv run python scripts/translation_management/compile_translations.py
```

### 3️⃣ **Quand tu ajoutes une nouvelle langue (par ex. allemand)**

```bash
# Créer le dossier
mkdir -p translations/de/LC_MESSAGES

# Copier le template
cp translations/template.pot translations/de/LC_MESSAGES/writing_assistant.po

# Synchroniser et compiler
uv run python scripts/translation_management/sync_translations.py
uv run python scripts/translation_management/compile_translations.py de
```

---

## 📁 Structure des traductions

```
translations/
├── template.pot              ← Template (source de vérité)
├── en/LC_MESSAGES/
│   ├── writing_assistant.po  ← Fichier éditable (EN)
│   └── writing_assistant.mo  ← Fichier compilé (EN)
├── fr/LC_MESSAGES/
│   ├── writing_assistant.po  ← Fichier éditable (FR)
│   └── writing_assistant.mo  ← Fichier compilé (FR)
└── it/LC_MESSAGES/
    ├── writing_assistant.po  ← Fichier éditable (IT)
    └── writing_assistant.mo  ← Fichier compilé (IT)
```

**À RETENIR :**
- `.pot` = Template (ne pas éditer)
- `.po` = Fichier éditable (c'est là qu'on met les traductions)
- `.mo` = Fichier compilé (utilisé par l'app)

---

## ✏️ Comment traduire ?

### Option 1 : Éditer les fichiers .po manuellement

Ouvre `translations/fr/LC_MESSAGES/writing_assistant.po` :

```po
msgid "Hello, this is a real desktop app!"
msgstr "Bonjour, c'est une vraie application desktop !"

msgid "Click me"
msgstr "Clique-moi"
```

Puis compile :
```bash
uv run python scripts/translation_management/compile_translations.py
```

### Option 2 : Utiliser un outil graphique

- **Poedit** (gratuit) : https://poedit.net/
- **GTranslator** : Outil GNOME

---

## 🔧 Commandes rapides

```bash
# Extraire tous les textes
uv run python scripts/translation_management/extract_translations.py

# Synchroniser toutes les langues
uv run python scripts/translation_management/sync_translations.py

# Compiler toutes les langues
uv run python scripts/translation_management/compile_translations.py

# Compiler une langue spécifique
uv run python scripts/translation_management/compile_translations.py fr

# Lister les langues disponibles
uv run python scripts/translation_management/compile_translations.py --list
```

---

## 🎯 Checklist pour ajouter une nouvelle langue

- [ ] Créer le dossier `translations/xx/LC_MESSAGES/`
- [ ] Copier `template.pot` → `writing_assistant.po`
- [ ] Lancer `sync_translations.py`
- [ ] Éditer le fichier `.po` avec les traductions
- [ ] Compiler avec `compile_translations.py xx`
- [ ] Tester dans l'app

---

## ⚠️ Dépannage

### "No Python files found" (extract fails)
✅ Assure-toi que le code est dans `src/` avec `_()` autour des textes

### "File not found" (sync fails)
✅ Vérifie que `translations/template.pot` existe

### Traductions ne s'affichent pas
✅ As-tu compilé avec `compile_translations.py` ?
✅ As-tu changé la langue dans `main.py` : `LANGUAGE = "fr"`

---

## 📝 Code : Comment utiliser les traductions dans l'app

```python
# Dans les fichiers Python
from src.core.translation import _

# Marquer du texte à traduire
ui.label(_("Texte à traduire"))
ui.button(_("Bouton"), on_click=lambda: ui.notify(_("Cliqué!")))

# Changer de langue à l'runtime
from src.core.translation import change_language
change_language("fr")  # Bascule à FR
```

---

## 📚 Structure du système de traduction

```
src/core/translation.py    ← Module principal (gère gettext)
                            ← init_translation() au démarrage
                            ← _() pour marquer les textes
                            ← change_language() pour basculer
```

---

**C'est tout ce que tu as besoin de savoir pour traduire l'app ! 🎯**
