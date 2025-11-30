# Roadmap (Feuille de Route)

Ce document recense les fonctionnalités planifiées et les améliorations techniques identifiées pour **Writing Assistant Pro**.

## ✅ Récemment Complété

- [x] **Refactoring UI** : Mise en place d'un Design System centralisé (`AppColors`, `AppTypography`) et composants réutilisables.
- [x] **Architecture** : Séparation claire `src/ui/components` et `src/ui/design_system.py`.

## 📅 Court Terme (Priorité Haute)

### 🛠️ Technique

- [ ] **Rotation des Logs** : Implémenter `loguru` rotation pour éviter les fichiers logs géants.
- [ ] **Tests Unitaires** : Augmenter la couverture de tests (actuellement minimale).
- [ ] **Nettoyage Code Mort** : Supprimer les anciens fichiers liés à NiceGUI ou PySide6 (si encore présents).

### ✨ Fonctionnalités

- [ ] **Raccourcis Clavier Globaux** : Finaliser l'implémentation pour afficher/masquer l'app depuis n'importe où.
- [ ] **Interface Paramètres** : Créer une UI complète pour modifier `config.json` sans éditer le fichier.

## 📅 Moyen Terme

### 🌍 Internationalisation

- [ ] **Support des Pluriels** : Implémenter `ngettext` pour gérer correctement les pluriels.
- [ ] **Détection Auto** : Détecter la langue du système au premier lancement.

### 📦 Distribution

- [ ] **Installeur Windows** : Créer un installeur `.msi` ou `setup.exe` (Inno Setup / NSIS).
- [ ] **Mise à jour Auto** : Système de vérification et téléchargement de mises à jour.
- [ ] **Signature de Code** : Signer l'exécutable pour éviter les avertissements SmartScreen.

## 📅 Long Terme (Vision)

### 🤖 Fonctionnalités IA

- **Interface Chat Moderne** : Une UI type ChatGPT/Claude fluide et réactive.
- **Historique de Conversation** : Persistance locale des échanges.
- **Support Multi-Modèles** : Connecteurs pour OpenAI, Anthropic, Ollama (local).

### 🔌 Extensibilité

- **Système de Plugins** : Architecture permettant d'ajouter des fonctionnalités sans toucher au cœur.
- **API Locale** : Serveur REST/Socket pour interagir avec d'autres outils.

## 🧪 Qualité & DevOps

- **CI/CD** : Pipeline GitHub Actions pour tests et builds automatiques.
- **Tests E2E** : Tests de bout en bout de l'interface graphique.
- **Documentation API** : Génération automatique de la doc technique.

---

> **Note** : Cette roadmap est un document vivant. Elle évolue en fonction des besoins et des retours utilisateurs.
