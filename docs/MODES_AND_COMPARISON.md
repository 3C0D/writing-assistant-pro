# Modes d'Exécution et Comparaison

Ce document décrit les trois modes d'exécution actuels du projet Writing Assistant Pro et les compare avec l'ancien projet (Legacy Project).

## Modes Actuels

### 1. `run_dev` (Mode Développement)

- **Commande** : `uv run python scripts/run_dev.py`
- **Description** : Lance l'application directement depuis le code source Python (`main.py`).
- **Caractéristiques** :
  - Argument `--debug` passé automatiquement à l'application.
  - **Copie systématique** des fichiers requis (assets) vers le dossier de distribution/dev avant lancement.
  - Configure `data_dev.json` comme fichier de données.
  - La console est visible pour les logs.
  - Utilise `uv` pour la gestion des dépendances.

### 2. `build_dev` (Build de Développement)

- **Commande** : `uv run python scripts/build_dev.py`
- **Description** : Crée un exécutable autonome pour le développement/test, situé dans `dist/dev/`.
- **Caractéristiques** :
  - Utilise **PyInstaller** en mode **onedir** (dossier contenant l'exécutable et les dépendances).
  - Peut être lancé en mode console (`--console`, par défaut) ou fenêtré (`--windowed`).
  - Copie les fichiers de configuration et assets "development".
  - Utilise `data_dev.json`.
  - Nettoie le cache PyInstaller uniquement si demandé explicitement (`--clean`).

### 3. `build_final` (Build de Production)

- **Commande** : `uv run python scripts/build_final.py`
- **Description** : Crée l'exécutable final pour la distribution, situé dans `dist/production/`.
- **Caractéristiques** :
  - Utilise **PyInstaller** en mode **onefile** (un seul fichier `.exe`).
  - Mode fenêtré uniquement (pas de console).
  - Copie les fichiers de configuration et assets "production".
  - Utilise `data.json` (production).
  - Optimisé pour la distribution utilisateur.

---

## Comparaison avec Legacy Project (PySide6)

L'analyse du projet Legacy (basé sur PySide6) révèle plusieurs différences de comportement et de fonctionnalités dans les scripts de gestion.

### Tableau des Différences

| Caractéristique                    | Mode Actuel (Flet)                          | Legacy Project (PySide6)                                                           | Analyse / Action Potentielle                                                                                                                                |
| :--------------------------------- | :------------------------------------------ | :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Framework UI**                   | Flet (Flutter)                              | PySide6 (Qt)                                                                       | Changement architectural majeur (prévu).                                                                                                                    |
| **`run_dev` : Copie des fichiers** | **Oui**, à chaque lancement.                | **Non**, uniquement via build ou manuel.                                           | Le comportement actuel est plus sûr pour garantir que les assets sont à jour. **À conserver.**                                                              |
| **`run_dev` : Argument Debug**     | **Oui** (`--debug` forcé).                  | **Non** (optionnel).                                                               | Utile pour le développement actuel. **À conserver.**                                                                                                        |
| **`build_dev` : Auto-Clean**       | **Non**, uniquement manuel (`--clean`).     | **Oui**, détection intelligente basée sur Git (si commit récent > 10min vs build). | La fonctionnalité "Auto-Clean" du Legacy était pratique pour éviter des builds corrompus après un `git pull`. **Suggestion : Réimplémenter cette logique.** |
| **Nom de l'exécutable**            | `Writing Assistant Pro`                     | `Writing Tools`                                                                    | Changement de nom voulu.                                                                                                                                    |
| **Gestion d'environnement**        | `uv` (moderne, rapide).                     | `venv` + scripts manuels (`utils.py`).                                             | `uv` simplifie grandement le code. **À conserver.**                                                                                                         |
| **Structure des données**          | `data_dev.json` (dev) / `data.json` (prod). | Identique.                                                                         | Cohérent.                                                                                                                                                   |

### Conclusions et Recommandations

1.  **Logique Globale** : La logique globale (3 modes) a été fidèlement reproduite.
2.  **Amélioration Legacy manquante** : La fonction `should_auto_clean` du script `build_dev.py` Legacy est absente du nouveau script. Elle permettait de nettoyer automatiquement le cache PyInstaller si des changements Git récents étaient détectés, évitant des erreurs de build subtiles.
    - _Action recommandée_ : Porter la fonction `should_auto_clean` vers le nouveau `build_dev.py`.
3.  **Robustesse `run_dev`** : Le nouveau script `run_dev.py` est plus robuste car il force la copie des assets, ce qui évite des erreurs "Asset not found" fréquentes lors du développement initial.

### Prochaines Étapes

- [ ] Réimplémenter la logique `should_auto_clean` dans `scripts/build_dev.py`.
- [ ] Vérifier que le `--debug` dans `run_dev` n'a pas d'effets de bord indésirables (ex: logs trop verbeux si non désirés).
