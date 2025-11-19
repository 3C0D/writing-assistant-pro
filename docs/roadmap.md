# Roadmap & Améliorations Futures

Ce document liste les améliorations techniques recommandées pour solidifier le projet et le rendre "Production Ready".

## 1. Gestion des Raccourcis Multi-plateforme ⌨️

**Problème actuel** : La librairie `keyboard` nécessite souvent les droits root (admin) sous Linux et macOS.
**Solution** :

- Migrer vers `pynput` ou `global-hotkeys`.
- Ces librairies respectent mieux les permissions utilisateur standard.
- Alternative : Gérer les raccourcis uniquement lorsque l'application a le focus (via NiceGUI/JS).

## 2. Packaging (Distribution) 📦

**Objectif** : Rendre l'application installable et exécutable sans avoir besoin d'installer Python manuellement.
**Outil** : `PyInstaller`.
**Actions** :

- Créer un fichier `writing-assistant.spec`.
- Configurer l'inclusion des assets (dossiers `src`, `translations`, `styles`).
- Générer les exécutables : `.exe` (Windows), `.app` (macOS), binaire (Linux).

## 3. Intégration Continue (CI/CD) 🤖

**Objectif** : Automatiser les tests et la vérification du code à chaque modification.
**Outil** : GitHub Actions.
**Actions** :

- Créer `.github/workflows/test.yml`.
- Étapes du workflow :
  1. Checkout du code.
  2. Installation de `uv` et Python.
  3. Installation des dépendances.
  4. Lancement de `ruff check` (linting).
  5. Lancement de `pytest` (tests unitaires).

## 4. Gestion Globale des Erreurs UI 🚨

**Objectif** : Éviter les crashs silencieux et informer l'utilisateur en cas de problème.
**Actions** :

- Implémenter un `Global Exception Handler` dans NiceGUI.
- Capturer les exceptions non gérées.
- Afficher une notification (Toast) conviviale : "Une erreur est survenue : [Détail]".
- Logger l'erreur complète pour le développeur.

## 5. Typage Statique (Type Hinting) 📏

**Objectif** : Renforcer la robustesse du code en détectant les erreurs de type avant l'exécution.
**Outil** : `mypy`.
**Actions** :

- Ajouter `mypy` aux dépendances de développement.
- Configurer `mypy.ini` ou `pyproject.toml`.
- Typer progressivement les fonctions clés (arguments et retours).
