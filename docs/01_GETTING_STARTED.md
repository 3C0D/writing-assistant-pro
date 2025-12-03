# Guide de Démarrage

## 👋 Bienvenue

Bienvenue dans la documentation de **Writing Assistant Pro**. Ce projet est une base solide pour une application de bureau moderne développée avec **Python** et **Flet**.

## 🚀 Installation Rapide

### Prérequis

- Windows 10/11 (Recommandé) ou Linux/macOS
- Python 3.10 ou supérieur
- [UV](https://docs.astral.sh/uv/) (Gestionnaire de projet Python moderne)

### Étapes

1. **Cloner le projet**

   ```bash
   git clone https://github.com/votre-repo/writing-assistant-pro.git
   cd writing-assistant-pro
   ```

2. **Installer les dépendances**

   ```bash
   uv sync
   ```

3. **Lancer l'application (Recommandé : Tâche VS Code)**

   - Ouvrir la palette de commandes : `Ctrl+Shift+P`
   - Sélectionner : `Tasks: Run Task` → `Run Dev`

   **Alternative (ligne de commande) :**

   ```bash
   uv run python scripts/dev_build/run_dev.py
   ```

## 🧭 Tour du Propriétaire

L'application se lance avec une interface moderne. Voici les fonctionnalités clés déjà en place :

- **Systray** : L'application vit dans la barre des tâches. Clic-droit sur l'icône pour le menu.
- **Logs** : Tout ce qui se passe est enregistré dans `logs/run_dev.log`.
- **Configuration** : Les paramètres sont sauvegardés dans `dist/dev/config.json`.
- **Traduction** : L'interface est prête pour le multi-langue (Anglais/Français/Italien...).

## 🛠️ Tâches VS Code Disponibles

**Recommandation :** Utilisez les tâches VS Code pour plus de simplicité !

Accès : `Ctrl+Shift+P` → `Tasks: Run Task` → Sélectionner la tâche

| Tâche                                   | Description                                |
| --------------------------------------- | ------------------------------------------ |
| **Run Dev**                             | Lancer l'application en mode développement |
| **Run Ruff**                            | Vérifier et corriger le code (linting)     |
| **Run Pyright**                         | Vérifier les types                         |
| **Build Dev**                           | Construire l'exécutable de développement   |
| **Build Final**                         | Construire l'exécutable de production      |
| **Commitizen: Create Commit**           | Créer un commit conventionnel              |
| **Commitizen: Bump Version**            | Créer une nouvelle version (release)       |
| **Commitizen: Bump Pre-release (Beta)** | Créer une pré-release (beta)               |

### Commandes Alternatives (Ligne de Commande)

Si vous préférez la ligne de commande :

| Action                 | Commande                                       |
| ---------------------- | ---------------------------------------------- |
| **Lancer (Dev)**       | `uv run python scripts/dev_build/run_dev.py`   |
| **Vérifier le code**   | `uv run python scripts/quality/run_ruff.py`    |
| **Vérifier les types** | `uv run python scripts/quality/run_pyright.py` |
| **Construire (Exe)**   | `uv run python scripts/dev_build/build_dev.py` |

## 📚 Où aller ensuite ?

- Pour comprendre comment développer : [Guide de Développement](./02_DEVELOPMENT.md)
- Pour voir comment fonctionne le build : [Système de Build](./03_BUILD_SYSTEM.md)
- Pour gérer les traductions : [Système de Traduction](./05_TRANSLATION.md)

## ❓ Besoin d'aide ?

Consultez les logs dans le dossier `logs/` ou référez-vous à la section [Dépannage](./02_DEVELOPMENT.md#dépannage) du guide de développement.
